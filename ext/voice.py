import discord
import youtube_dl
from discord.ext import commands
from subprocess import Popen
import aiohttp
import os
import asyncio

class voice:
    def __init__(self, client):
        self.client = client
        self.players = {}

    @commands.command(pass_context=True)
    async def join(self, ctx):
        self.channel = ctx.message.author.voice.voice_channel
        await self.client.join_voice_channel(self.channel)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        self.server = ctx.message.server
        self.voice_client = self.client.voice_client_in(self.server)
        await self.voice_client.disconnect()

#---------------------------------------------YOUTUBE---------------------------------------------------------------------------------
    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        self.server = ctx.message.server
        self.voice_client = self.client.voice_client_in(self.server)
        if self.voice_client == None:
            self.voice_client = await self.client.join_voice_channel(ctx.message.author.voice.voice_channel)    
        self.player = await self.voice_client.create_ytdl_player(url)
        self.players[self.server.id] = self.player
        self.player.start()
    
    @commands.command(pass_context=True)
    async def pause(ctx):
        self.players[ctx.message.server.id].pause()

    @commands.command(pass_context=True)
    async def resume(ctx):
        self.players[ctx.message.server.id].resume()

    @commands.command(pass_context=True)
    async def stop(ctx):
        self.players[ctx.message.server.id].stop()

    @commands.command(pass_context=True)
    async def ytdl(self, ctx, url):
        msg = await self.client.say("Nep is trying her hardest to get your file. https://i.kym-cdn.com/photos/images/original/001/283/141/58e.gif")
        process = Popen(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "-o", "output.%(ext)s", url], shell=False)
        process.wait()
        session = aiohttp.ClientSession()
        upload = open("output.mp3", "rb")
        files = {'filedata': upload}
        resp = await session.post('https://transfer.sh/', data=files)
        upload.close()
        os.remove("output.mp3")
        session.close()
        await self.client.edit_message(msg, await resp.text())
        msg, process, session, upload, files, resp = None, None,None,None,None,None



def setup(client):
    discord.opus.load_opus("vendor/lib/libopus.so.0")
    if discord.opus.is_loaded():
        print("Opus loaded!")

    client.add_cog(voice(client))