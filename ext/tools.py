import discord
from discord.ext import commands
from ext.database import database

class tools:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def audit(self, ctx, chan=None):
        if chan is None:
            C = ctx.message.channel
        else:
            C = self.client.get_channel(int(chan))
        with open(f"{C.id}.txt", "w") as output:
            async for msg in C.history():
                output.write(f"{msg.author} : {msg.content} \n")
            output.flush()
            database.sendFile(self, ctx, output)



    
def setup(client):
    client.add_cog(tools(client))
