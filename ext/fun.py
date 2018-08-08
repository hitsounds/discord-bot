import discord
from discord.ext import commands
import random

class fun:
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    async def bws(self, ctx):
        async for self.message in self.client.logs_from(id(320320664085069824), limit=10):
            print(self.message.clean_content)
            
#        await self.client.send_message(ctx.message.channel, self.bw(random.randint(1,5500)))

    @commands.command()
    async def ping():
        await self.client.say("Pong!")


def setup(client):
    client.add_cog(fun(client))