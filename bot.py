import discord
from discord.ext import commands
import os

#The import os and token are setup for Heroku if you want to host locally you can just remove the import os and set "TOKEN" to your bot's token
TOKEN = os.environ.get('TOKEN')

client = commands.Bot(command_prefix = ";")
extensions = os.fsencode("ext/")


"""Opus was a pain to install on heroku but the following line is probs not needed if running on windows
   Opus is a must for the join and leave commands as well as if you intend to add music to the bot"""
discord.opus.load_opus("vendor/lib/libopus.so.0")


if discord.opus.is_loaded():
    print("opus")
else:
    print("no opus")

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="Nothing",type = 1))
    print ("Bot is ready")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command(pass_context=True)
async def me(ctx):
    await client.say("HI")

#@client.command(pass_context=True)
#async def join(ctx):
#    channel = ctx.message.author.voice.voice_channel
#    await client.join_voice_channel(channel)

#@client.command(pass_context=True)
#async def leave(ctx):
#    server = ctx.message.server
#    voice_client = client.voice_client_in(server)
#    await voice_client.disconnect()

for file in os.listdir(extensions):
    try:
        client.load_extension(os.fsdecode(file).replace(".py",""))
    except Exception as error:
        print(error)   


client.run(TOKEN)
