import discord
from discord.ext import commands

from config import ARRIVAL_CHANNEL, LEAVE_CHANNEL
from utils import find_text_channel


class Welcome(commands.Cog):
    """Messages d'arrivée et de départ."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ch = find_text_channel(member.guild, ARRIVAL_CHANNEL)
        if ch:
            embed = discord.Embed(
                title="👋 Bienvenue !",
                description=f"{member.mention} nous rejoint ! Pense à lire le règlement.\n"
                f"Nous sommes maintenant **{member.guild.member_count}** membres.",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        ch = find_text_channel(member.guild, LEAVE_CHANNEL)
        if ch:
            embed = discord.Embed(
                title="📤 Départ",
                description=f"**{member.display_name}** a quitté le serveur.",
                color=discord.Color.red(),
            )
            await ch.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))
