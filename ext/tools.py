#General useful stuff

import discord
from discord.ext import commands
class misc(commands.Cog):

	def init(self, client):
		self.client = client

	@commands.command(name="sharescreen", aliases=["sss","serversharescreen"])
	async def sss_(self, ctx):
		try:
			channel = ctx.author.voice.channel
		except AttributeError:
			await ctx.send("Join a voice channel and use this command to start a share screen session.")
			return
		embed=discord.Embed(title=f"Share Screen Link for: {channel.name}", description=f"[Start Share Screen](https://discordapp.com/channels/{ctx.message.guild.id}/{channel.id})")
		await ctx.send(embed=embed)

	

def setup(client):
	client.add_cog(misc(client))
