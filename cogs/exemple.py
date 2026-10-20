import discord
from discord.ext import commands

from config import GUILD_ID

# ─────────────────────────────────────────────────────────────
# COMMENT AJOUTER UNE COMMANDE ?
#   1. Copie ce fichier dans le dossier cogs/ (ex: cogs/ma_commande.py)
#   2. Change le nom de la classe et de la commande
#   3. Relance le bot : tous les fichiers de cogs/ sont chargés automatiquement
# ─────────────────────────────────────────────────────────────


class Exemple(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Teste si le bot répond", guild_ids=[GUILD_ID])
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"🏓 Pong ! {round(self.bot.latency * 1000)} ms", ephemeral=True)


def setup(bot):
    bot.add_cog(Exemple(bot))
