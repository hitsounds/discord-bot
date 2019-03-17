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
		await self.client.loop.run_in_executor(None, dlr.aio_initalise)
		while dlr.playlist and not dlr.finished:
			file = await self.client.loop.run_in_executor(None, dlr.dl)
			with open(file, "rb") as fl:
				resp = await lib.sendfile(fl, d_ctx=ctx)
			if isinstance(resp, str):
				await ctx.send(resp)
		file = await self.client.loop.run_in_executor(None, dlr.dl)
		with open(file, "rb") as fl:
			resp = await lib.sendfile(fl, d_ctx=ctx)
		if isinstance(resp, str):
			await ctx.send(resp)
		dlr.cleanup()


def setup(client):
	client.add_cog(misc(client))
