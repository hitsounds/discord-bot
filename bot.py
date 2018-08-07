import discord
from discord.ext import commands
#from boto.s3.connection import S3Connection
import os

TOKEN = os.environ.get['TOKEN']

client = commands.Bot(command_prefix = ";hs;")

@client.event
async def on_ready():
    print ("Bot is ready")

client.run(TOKEN)
