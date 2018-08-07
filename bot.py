import discord
from discord.ext import commands
import os

TOKEN = os.environ.get('TOKEN')

client = commands.Bot(command_prefix = ";hs;")

@client.event
async def on_ready():
    print ("Bot is ready")

client.run(TOKEN)
