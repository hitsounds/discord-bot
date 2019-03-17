import io
import aiohttp
import os
import discord


async def file_from_url(url):
	async with aiohttp.ClientSession() as session:
		resp = await session.get(url)
		return io.BytesIO(await resp.read())


async def sendfile(fileobj, *, d_ctx=None, filename=None, spoiler=False):
	if os.fstat(fileobj.fileno()).st_size/1048576. < 7 and d_ctx != None:
		return await d_ctx.send(file=discord.File(fileobj))
	elif os.fstat(fileobj.fileno()).st_size/1048576. < 99:
		async with aiohttp.ClientSession() as session:
			resp = await session.post("https://uguu.se/api.php?d=upload-tool", data={"file": fileobj})
		return resp.text
	elif os.fstat(fileobj.fileno()).st_size/1048576. < 510.:
		async with aiohttp.ClientSession() as session:
			resp = await session.post("https://0x0.st", data={"file": fileobj})
		return resp.text
	else:
		async with aiohttp.ClientSession() as session:
			resp = await session.post("https://transfer.sh", data={"file": fileobj})
		return resp.text
