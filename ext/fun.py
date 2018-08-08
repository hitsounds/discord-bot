import discord
from discord.ext import commands
import random

class fun:
    def __init__(self, client):
        self.client = client
        self.bws = client.logs_from("320320664085069824")

    @commands.command(pass_context=True)
    async def bws(self, ctx):
        await self.client.send_message(ctx.message.channel,random.choice(self.bws))

def setup(client):
    client.add_cog(fun(client))