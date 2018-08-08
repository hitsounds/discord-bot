import discord
import youtube_dl
from discord.ext import commands

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

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        self.server = ctx.message.server
        self.voice_client = self.client.voice_client_in(self.server)
        self.player = await self.voice_client.create_ytdl_player(url)
        self.players[self.server.id] = self.player
        self.player.start()


def setup(client):
    discord.opus.load_opus("vendor/lib/libopus.so.0")
    if discord.opus.is_loaded():
        print("Opus loaded!")

    client.add_cog(voice(client))