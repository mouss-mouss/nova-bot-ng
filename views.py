import asyncio

import discord

from config import PREFIX
from utils import PO, ensure_category, staff_roles


class TicketClose(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        btn = discord.ui.Button(
            label="🔒 Fermer le ticket",
            style=discord.ButtonStyle.danger,
            custom_id="nova:close",
        )
        btn.callback = self.close_ticket
        self.add_item(btn)

    async def close_ticket(self, interaction: discord.Interaction):
        channel = interaction.channel
        topic = channel.topic or ""
        if not topic.startswith("ticket:"):
            await interaction.response.send_message("❌ Ce n'est pas un ticket.", ephemeral=True)
            return
        owner_id = int(topic.split(":")[2])
        can_manage = channel.permissions_for(interaction.user).manage_messages
        if interaction.user.id != owner_id and not can_manage:
            await interaction.response.send_message(
                "❌ Seuls le créateur du ticket et le staff peuvent le fermer.", ephemeral=True
            )
            return
        await interaction.response.send_message("🔒 Fermeture du ticket dans 5 secondes...")
        await asyncio.sleep(5)
        await channel.delete(reason=f"Ticket fermé par {interaction.user}")


class TicketPanel(discord.ui.View):
    def __init__(self, kind, type_name):
        super().__init__(timeout=None)
        self.kind = kind
        self.type_name = type_name
        label = "📝 Postuler" if kind == "recrutement" else "🛒 Passer commande"
        btn = discord.ui.Button(
            label=label,
            style=discord.ButtonStyle.primary,
            custom_id=f"nova:open:{kind}:{type_name}",
        )
        btn.callback = self.open_ticket
        self.add_item(btn)

    async def open_ticket(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild, user = interaction.guild, interaction.user

        roles = staff_roles(guild, self.kind, self.type_name)
        if not roles:
            await interaction.followup.send(
                "❌ Rôles introuvables, un admin doit lancer /setup-entreprises.", ephemeral=True
            )
            return

        me_ow = PO(view_channel=True, send_messages=True, manage_channels=True, manage_messages=True)
        cat_name = f"🎫・{PREFIX.upper()} TICKETS {self.type_name.upper()}"
        category, _ = await ensure_category(
            guild, cat_name, {guild.default_role: PO(view_channel=False), guild.me: me_ow}
        )

        topic = f"ticket:{self.kind}:{user.id}"
        for c in category.text_channels:
            if c.topic == topic:
                await interaction.followup.send(f"📌 Tu as déjà un ticket ouvert : {c.mention}", ephemeral=True)
                return

        overwrites = {
            guild.default_role: PO(view_channel=False),
            user: PO(view_channel=True, send_messages=True, attach_files=True, read_message_history=True),
            guild.me: me_ow,
        }
        for r in roles:
            overwrites[r] = PO(
                view_channel=True,
                send_messages=True,
                attach_files=True,
                read_message_history=True,
                manage_messages=True,
            )

        channel = await category.create_text_channel(
            name=f"{self.kind}-{user.name}", topic=topic, overwrites=overwrites
        )

        if self.kind == "recrutement":
            embed = discord.Embed(
                title=f"📝 Candidature {PREFIX} {self.type_name}",
                description="Présente-toi : pseudo en jeu, expérience, disponibilités et motivation.\n"
                "La direction te répondra ici.",
                color=discord.Color.blurple(),
            )
        else:
            embed = discord.Embed(
                title=f"🛒 Commande {PREFIX} {self.type_name}",
                description="Décris ta commande : ce que tu veux, quantité, délai et prix proposé.\n"
                "Un employé te répondra ici.",
                color=discord.Color.green(),
            )
        mentions = " ".join([user.mention] + [r.mention for r in roles])
        await channel.send(content=mentions, embed=embed, view=TicketClose())
        await interaction.followup.send(f"✅ Ticket créé : {channel.mention}", ephemeral=True)
