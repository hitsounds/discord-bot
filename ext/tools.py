import discord
from discord.ext import commands
from ext.database import database
import os
import re

class tools:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def audit(self, ctx, chan=None):
        async with ctx.message.channel.typing():
            if chan is None:
                C = ctx.message.channel
            else:
                C = self.client.get_channel(int(chan))
            with open(f"{C.id}.txt", "w") as output:
                output.write("time | author name | author id | content | attachments | URL\n")
                async for msg in C.history(limit=None, reverse=True):
                    output.write(f"{msg.created_at} | {msg.author.name} | {msg.author.id} | \"{msg.clean_content.replace("\"","\'")}\" |")
                    for i in msg.attachments: output.write(f" {i.proxy_url} ")
                    output.write(f"| {msg.jump_url}\n")
            with open(f"{C.id}.txt", "rb") as output:
                await database.sendFile(self, ctx, output)
            os.remove(f"{C.id}.txt")



    
def setup(client):
    client.add_cog(tools(client))
