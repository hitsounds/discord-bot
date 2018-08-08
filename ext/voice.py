import discord
from discord.ext import commands

class voice:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def join(self, ctx):
        self.channel = ctx.message.author.voice.voice_channel
        await client.join_voice_channel(self.channel)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        self.server = ctx.message.server
        self.voice_client = self.client.voice_client_in(server)
        await self.voice_client.disconnect()    

def setup(client):
    client.add_cog(voice(client))