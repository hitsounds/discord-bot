import discord
from discord.ext import commands
import os

TOKEN = os.environ.get('TOKEN')

cogs_dir = "ext"
i_cogs = []

client = commands.Bot(command_prefix = ";")
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name=";help", type=discord.ActivityType(2)))
    print ("Bot is ready")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.get_channel(426816759648092160).send("Ready when you are! <@130025130100391936>")

@client.command()
async def me(ctx):
    await ctx.say("HI")

    
@client.command()
async def help(ctx):
    await ctx.message.delete()
    await ctx.send("https://goo.gl/vya4Sp")



#loading the extensions from ext/ folder
for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            client.load_extension(cogs_dir + "." + extension)
            print ("{} module loaded!".format(extension))
            i_cogs.append(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.') 
            print (e)

client.run(TOKEN)
