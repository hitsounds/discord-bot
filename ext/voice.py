import discord
import youtube_dl
from discord.ext import commands
import aiohttp
import os
import asyncio
from ext.database import database
import random

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data: data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename), data=data)



class voice:
    def __init__(self, client):
        self.client = client
        self.voiceCs = {}

    @commands.command()
    async def join(self, ctx):
        self.voiceCs[ctx.guild.id] = await ctx.message.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await self.voiceCs[ctx.guild.id].disconnect()

    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.play(await YTDLSource.from_url(url))


#---------------------------------------------YOUTUBE---------------------------------------------------------------------------------
    @commands.command()
    async def ytdl(self, ctx, url, Cext="mp3"):
        msg = await ctx.send("Nep is trying her hardest to get your file. https://i.kym-cdn.com/photos/images/original/001/283/141/58e.gif")
        name = random.getrandbits(64)
        if Cext == "mp4":
            Cext = "mp4"
            process = await asyncio.create_subprocess_shell("youtube-dl --no-playlist --default-search \"ytsearch\" -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio' --merge-output-format mp4 -o {}.mp4 \"{}\"".format(name, url), stdout=asyncio.subprocess.PIPE)
            await process.communicate()
        else:
            Cext = "mp3"
            process = await asyncio.create_subprocess_shell("youtube-dl --no-playlist --default-search \"ytsearch\" --embed-thumbnail --audio-quality 0 --extract-audio --audio-format mp3 -o {}.mp3 \"{}\"".format(name,url), stdout=asyncio.subprocess.PIPE)
            await process.communicate()
        with open(f"{name}.{Cext}", "rb") as f:
            await database.sendFile(self, ctx, f)
        os.remove(f"{name}.{Cext}")
        await msg.delete()




def setup(client):
    discord.opus.load_opus("vendor/lib/libopus.so.0")
    if discord.opus.is_loaded():
        print("Opus loaded!")
    client.add_cog(voice(client))
