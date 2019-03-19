# Commands to extract the good stuffs

import discord
from discord.ext import commands
import youtube_dl
import asyncio
import lib
from functools import partial


class misc(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(name="ytdl", aliases=["dl"])
	async def ytdl_(self, ctx, *, url: str):
		dlr = lib.ytdl.ytdl_downloader(url)
		embed = discord.Embed(title="Processing the file!", description="Processing will take longer on playlist downloads.")
		embed.set_image(url="https://media.giphy.com/media/PPxgdzGdl8BJm/giphy.gif")
		embed.set_footer(text=f"Args: {dlr.search}  Mods: {dlr.mods}")
		msg = await ctx.send(embed=embed)
		await self.client.loop.run_in_executor(None, dlr.aio_initalise)
		embed = discord.Embed(title="Downloading!", description=f"ID : {dlr.id}")
		embed.set_image(url="https://i.pinimg.com/originals/a6/4e/ff/a64eff819ce5a97596db56af45daba63.gif")
		embed.set_footer(text=f"Args: {dlr.search}  Mods: {dlr.mods}")
		await msg.edit(embed=embed)
		while dlr.is_playlist and dlr.playlist and not dlr.finished:
			file = await self.client.loop.run_in_executor(None, dlr.dl)
			with open(file, "rb") as fl:
				resp = await lib.sendfile(fl, d_ctx=ctx)
			if isinstance(resp, str):
				await ctx.send(resp)
		if not dlr.playlist or not dlr.is_playlist:
			file = await self.client.loop.run_in_executor(None, dlr.dl)
			with open(file, "rb") as fl:
				resp = await lib.sendfile(fl, d_ctx=ctx)
			if isinstance(resp, str):
				await ctx.send(resp)
		dlr.cleanup()


def setup(client):
	client.add_cog(misc(client))
