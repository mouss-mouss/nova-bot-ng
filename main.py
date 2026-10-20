import os

import discord

from config import TOKEN

intents = discord.Intents.default()
intents.members = True  # nécessaire pour arrivée/départ (à activer dans le portail développeur)
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")


# Charge automatiquement tous les fichiers du dossier cogs/
for filename in sorted(os.listdir("cogs")):
    if filename.endswith(".py") and not filename.startswith("_"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"Cog chargé : {filename[:-3]}")

bot.run(TOKEN)
