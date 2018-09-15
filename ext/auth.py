import discord
from discord.ext import commands
import aiohttp
import asyncio
import psycopg2
from ext.database import database
import os

class discord_auth:
    def __init__(self, client):
        self.client = client
    
    @commands.group()
    async def auth(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.author.send("Please select a service to authorise", delete_after=5.0)
        
    
    @auth.command()
    async def discord(self, ctx):
        await ctx.message.author.send(r"<https://discordapp.com/api/oauth2/authorize?client_id=476383348969963531&redirect_uri=https%3A%2F%2Fdicsordbot.herokuapp.com&response_type=code&scope=identify%20email%20connections%20guilds%20guilds.join>")
        await ctx.message.author.send("Click the above link. Authorise the bot and then send the redirect link to me! This will timeout in 30 secs.")
        def check(m):
            return m.content.startswith("https://dicsordbot.herokuapp.com/?code=") or m.content.startswith("dicsordbot.herokuapp.com/?code=")
        try:
            msg = await self.client.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.message.author.send("I'm done waiting.")
        else:
            code = msg.content.split("?code=")[1]
            print(code)
            data = {
                'client_id': self.client.user.id,
                'client_secret': os.environ["discord_client_secret"],
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': "https://dicsordbot.herokuapp.com",
                'scope': 'connections identify email guilds guilds.join'
            }
            async with aiohttp.ClientSession() as session:
                resp = await session.post("https://discordapp.com/api/oauth2/token", params=data)
                resp = await resp.json()
                print(resp)








def setup(client):
    client.add_cog(discord_auth(client))
