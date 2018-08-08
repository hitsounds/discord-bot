import discord
from discord.ext import commands
import random

class fun:
    def __init__(self, client):
        self.client = client
        self.bws = []
        async for self.message in self.client.logs_from(self.client.get_channel("320320664085069824"), limit=5500):
            self.bws.append(self.message.clean_content)
    
    @commands.command(pass_context=True)
    async def bws(self, ctx):
        await self.client.send_message(ctx.message.channel, random.choice(self.bws))

            
#        await self.client.send_message(ctx.message.channel, self.bw(random.randint(1,5500)))

    @commands.command()
    async def ping():
        await self.client.say("Pong!")


def setup(client):
    client.add_cog(fun(client))