import discord
from discord.ext import commands
import os

#The import os and token are setup for Heroku if you want to host locally you can just remove the import os and set "TOKEN" to your bot's token
TOKEN = os.environ.get('TOKEN')

client = commands.Bot(command_prefix = ";hs;")

@client.event
async def on_ready():
    print ("Bot is ready")
    print('Logged in as')
    print(client.user.name)
    print(clent.user.id)
    print('------')


client.run(TOKEN)
