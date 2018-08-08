import discord
from discord.ext import commands
import os

#The import os and token are setup for Heroku if you want to host locally you can just remove the import os and set "TOKEN" to your bot's token
TOKEN = os.environ.get('TOKEN')

client = commands.Bot(command_prefix = ";")
discord.opus.load_opus("opus")

@client.event
async def on_ready():
    print ("Bot is ready")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command(pass_context=True)
async def me(ctx):
    await client.say("HI")

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

client.run(TOKEN)
