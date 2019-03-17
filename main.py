import discord
from discord.ext import commands
import lib
import asyncio
import os
import sqlalchemy
import random
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from shutil import copyfile

try:
	import config
except ImportError:
	copyfile("config.py.template", "config.py")
	print("config.py file created. If you are using enviromental variables you can ignore this otherwise make sure to check out the config if you are having trouble")
	import config

# Set-up persistent storage
if not os.path.isdir("persist"):
	os.mkdir("persist")

# Client setup
status_messages = ["Tea Party with Abijith", "it slow"]
client = commands.Bot(command_prefix=commands.when_mentioned_or(";"))
client.remove_command("help")

# Database setup
base = declarative_base()


class users(base):
	__tablename__ = 'users'
	discord_id = sqlalchemy.Column(sqlalchemy.String, nullable=False, primary_key=True)
	osu_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)

	def __init__(self, id):
		self.discord_id = id


if config.DB_URL is None:
	db = sqlalchemy.create_engine("sqlite:///persist/bot.db")
else:
	db = sqlalchemy.create_engine(config.DB_URL)

client.DATABASE_SESSIONMAKER = sessionmaker(db)
base.metadata.create_all(db, checkfirst=True)
client.DATABASE_BASE = base

# Message on ready
@client.event
async def on_ready():
	print("Bot is ready")
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

# Add people to database
@client.command()
async def scan(ctx):
	session = client.DATABASE_SESSIONMAKER()
	for i in ctx.message.guild.members:
		test = session.query(users).filter(
			users.discord_id == str(i.id)).first()
		if not test:
			member = session.add(users(str(i.id)))
	session.commit()
	session.close()
	await ctx.send("Scan success!")

# Random discord rich presence


async def update_status_msg():
	await client.wait_until_ready()
	while not client.is_closed():
		await client.change_presence(activity=discord.Game(name=random.choice(status_messages)))
		await asyncio.sleep(900)

# Load extensions from ext/ dir
for ext in [i.replace('.py', '') for i in os.listdir("ext") if os.path.isfile(os.path.join("ext", i))]:
	try:
		client.load_extension(f"ext.{ext}")
	except Exception as e:
		print(f"Error in loading {ext}\n{e}")

# try to load the libopus
# discord.opus.load_opus("libopus.so.0")

# Run client
client.loop.create_task(update_status_msg())
client.run(config.DISCORD_TOKEN)
