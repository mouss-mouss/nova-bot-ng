from discord.ext import commands

from config import COMPANY_TYPES
from views import TicketClose, TicketPanel


class Tickets(commands.Cog):
    """Réenregistre les boutons de tickets au démarrage (ils survivent aux redémarrages)."""

    def __init__(self, bot):
        self.bot = bot
        self._ready = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self._ready:
            return
        self.bot.add_view(TicketClose())
        for t in COMPANY_TYPES:
            for kind in ("recrutement", "commande"):
                self.bot.add_view(TicketPanel(kind, t["name"]))
        self._ready = True


def setup(bot):
    bot.add_cog(Tickets(bot))
