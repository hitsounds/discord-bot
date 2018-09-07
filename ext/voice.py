import discord
import youtube_dl
from discord.ext import commands
import aiohttp
import os
import asyncio
from ext.database import database
import random
import functools

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()
        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]
        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)



class voice:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.message.author.voice.channel)
        await ctx.message.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        async with ctx.typing():
            source = await YTDLSource.create_source(ctx, url, loop=self.client.loop)
            player = await YTDLSource.regather_stream(source, loop=self.client.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))


    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


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
