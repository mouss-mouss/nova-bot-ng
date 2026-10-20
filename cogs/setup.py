import discord
from discord.ext import commands

from config import (
    COMPANY_TYPES,
    EMPLOYEE_CHANNELS,
    GLOBAL_CATEGORIES,
    GUILD_ID,
    PREFIX,
    PUBLIC_CHANNELS,
    RULES,
)
from utils import build_overwrites, ensure_category, ensure_channel, post_once, role_names
from views import TicketPanel


class Setup(commands.Cog):
    """Commande /setup-entreprises : crée accueil, global et les branches."""

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="setup-entreprises",
        description="Crée accueil, global, et les catégories/rôles/tickets de chaque entreprise",
        guild_ids=[GUILD_ID],
        default_member_permissions=discord.Permissions(administrator=True),
    )
    async def setup_entreprises(self, ctx: discord.ApplicationContext):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("❌ Réservé aux admins.", ephemeral=True)
            return

        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        created = 0
        panels = 0

        try:
            # ── 1) Accueil + Global ──
            for cat in GLOBAL_CATEGORIES:
                category, new = await ensure_category(guild, cat["name"])
                created += new
                for ch in cat["channels"]:
                    channel, new = await ensure_channel(guild, category, ch, [], locked=False)
                    created += new
                    if ch.get("rules"):
                        embed = discord.Embed(
                            title="📜 Règlement",
                            description="\n".join(f"**{i}.** {r}" for i, r in enumerate(RULES, 1)),
                            color=discord.Color.gold(),
                        )
                        panels += await post_once(channel, embed)

            # ── 2) Une branche par type d'entreprise ──
            for ctype in COMPANY_TYPES:
                name = ctype["name"]
                emoji = ctype.get("emoji", "🏢")

                # Rôles : Employé + Direction
                roles = []
                for rname in role_names(name):
                    role = discord.utils.get(guild.roles, name=rname)
                    if role is None:
                        role = await guild.create_role(name=rname, mentionable=True)
                        created += 1
                    roles.append(role)

                # Catégorie publique
                public_cat, new = await ensure_category(
                    guild, f"{emoji}・{PREFIX.upper()} {name.upper()}"
                )
                created += new
                for ch in PUBLIC_CHANNELS:
                    channel, new = await ensure_channel(guild, public_cat, ch, roles, locked=False)
                    created += new

                    kind = ch.get("panel")
                    if kind:
                        if not new:
                            # salon déjà existant : on le passe en lecture seule pour le panneau
                            await channel.set_permissions(guild.default_role, send_messages=False)
                            await channel.set_permissions(
                                guild.me, view_channel=True, send_messages=True, embed_links=True
                            )
                        if kind == "recrutement":
                            embed = discord.Embed(
                                title=f"📝 Recrutement {PREFIX} {name}",
                                description="Clique sur le bouton pour ouvrir un ticket privé avec la direction.",
                                color=discord.Color.blurple(),
                            )
                        else:
                            embed = discord.Embed(
                                title=f"🛒 Commandes {PREFIX} {name}",
                                description="Clique sur le bouton pour ouvrir un ticket privé avec nos employés.",
                                color=discord.Color.green(),
                            )
                        panels += await post_once(channel, embed, TicketPanel(kind, name))

                # Catégorie employés verrouillée (employés + direction)
                emp_cat, new = await ensure_category(
                    guild,
                    f"👥・{PREFIX.upper()} EMPLOYÉS {name.upper()}",
                    build_overwrites(guild, roles, False, locked=True),
                )
                created += new
                for ch in EMPLOYEE_CHANNELS:
                    _, new = await ensure_channel(guild, emp_cat, ch, roles, locked=True)
                    created += new

            await ctx.followup.send(
                f"✅ Terminé : {created} élément(s) créé(s), {panels} panneau(x) posté(s). "
                "Ce qui existait déjà n'a pas été recréé.",
                ephemeral=True,
            )
        except discord.Forbidden:
            await ctx.followup.send(
                "❌ Il me manque des permissions (Gérer les salons / Gérer les rôles), "
                "et mon rôle doit être placé au-dessus des rôles Nova.",
                ephemeral=True,
            )
        except Exception as e:
            print(e)
            await ctx.followup.send("❌ Une erreur est survenue, regarde la console.", ephemeral=True)


def setup(bot):
    bot.add_cog(Setup(bot))
