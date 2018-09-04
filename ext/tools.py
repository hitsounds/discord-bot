import discord
from discord.ext import commands
from ext.database import database
import os

class tools:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def audit(self, ctx, chan=None):
        async with ctx.message.channel.typing():
            if chan is None:
                C = ctx.message.channel
            else:
                C = await self.client.get_channel(int(chan))
            with open(f"{C.id}.txt", "w") as output:
                async for msg in C.history():
                    output.write(f"{msg.author} : {msg.content} \n")
            with open(f"{C.id}.txt", "rb") as output:
                await database.sendFile(self, ctx, output)
            os.remove(f"{C.id}.txt")



    
def setup(client):
    client.add_cog(tools(client))
