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
    await client.change_presence(game=discord.Game(name=";help",type = 0))
    print ("Bot is ready")
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.send_message("426816759648092160", "Ready when you are! <@130025130100391936>")

@client.command(pass_context=True)
async def me(ctx):
    await client.say("HI")

    
@client.command(pass_context=True)
async def help(ctx):
    await client.delete_message(ctx.message)
    await client.send_message(ctx.message.author, "https://goo.gl/vya4Sp"  )



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
