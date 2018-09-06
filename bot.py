import discord
from discord.ext import commands
import os
import asyncio
import random


TOKEN = os.environ.get('TOKEN')
cogs_dir = "ext"
i_cogs = []
status_messages = ["Tea Party with Abijith", "the piano", "UP", ";help", "Osu!", "without limits", "hard mode"]

client = commands.Bot(command_prefix = [";","<@476383348969963531> "])
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name=";help", type=discord.ActivityType(3)))
    print ("Bot is ready")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.get_channel(426816759648092160).send("Ready when you are! <@130025130100391936>")


@client.command()
async def me(ctx):
    await ctx.send("HI")

    
@client.command()
async def help(ctx):
    await ctx.message.delete()
    await ctx.send("https://goo.gl/vya4Sp")

async def status_msg():
    while not client.is_closed():
        await asyncio.sleep(900)
        await client.change_presence(activity=discord.Game(name=random.choice(status_messages)))




#loading the extensions from ext/ folder
for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            client.load_extension(cogs_dir + "." + extension)
            print ("{} module loaded!".format(extension))
            i_cogs.append(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.') 
            print (e)

client.loop.create_task(status_msg())
client.run(TOKEN)
