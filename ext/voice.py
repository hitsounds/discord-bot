import discord
import youtube_dl
from discord.ext import commands
import aiohttp
import os
import asyncio
from ext.database import database
import random

class voice:
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
        self.voiceCs = {}

    @commands.command()
    async def join(self, ctx):
        self.voiceCs[ctx.guild.id] = await ctx.message.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        self.voiceCs[ctx.guild.id].disconnect()

#---------------------------------------------YOUTUBE---------------------------------------------------------------------------------
    @commands.command()
    async def ytdl(self, ctx, url, ext="mp3"):
        msg = await ctx.send("Nep is trying her hardest to get your file. https://i.kym-cdn.com/photos/images/original/001/283/141/58e.gif")
        name = random.getrandbits(64)
        if ext == "mp4":
            process = await asyncio.create_subprocess_shell("youtube-dl --default-search \"ytsearch\" -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio' --merge-output-format mp4 -o {}.mp4 {}".format(name, url), stdout=asyncio.subprocess.PIPE)
            await process.communicate()
        else:
            ext = "mp3"
            process = await asyncio.create_subprocess_shell("youtube-dl --default-search \"ytsearch\" --embed-thumbnail --audio-quality 0 --extract-audio --audio-format mp3 -o {}.mp3 {}".format(name,url), stdout=asyncio.subprocess.PIPE)
            await process.communicate()
        await database.sendFile(self, ctx, name, ext)
        await msg.delete()




def setup(client):
    discord.opus.load_opus("vendor/lib/libopus.so.0")
    if discord.opus.is_loaded():
        print("Opus loaded!")
    client.add_cog(voice(client))
