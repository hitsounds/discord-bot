import discord
from discord.ext import commands
import aiohttp
import asyncio
import psycopg2
from ext.database import database
import os
from libs.lib import config

class discord_auth:
    def __init__(self, client):
        self.client = client
        self.cs =config.get("discord_client_secret")
        
    
    @commands.group()
    async def auth(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.author.send("Please select a service to authorise", delete_after=5.0)
        
    
    @auth.command()
    async def discord(self, ctx):
        await ctx.message.author.send("https://api.hitsounds.moe/discord/login")









def setup(client):
    client.add_cog(discord_auth(client))
