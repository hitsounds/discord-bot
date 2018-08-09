import os
import psycopg2
import discord
from discord.ext import commands

class database:
    def __init__(self, client):
        self.client = client
        self.conn = None

    @commands.command()
    async def tablec(self):
        self.load()
        self.cur = self.conn.cursor()
        self.cur.close()
        self.unload()

    @commands.group(pass_context=True)
    async def db(self, ctx):
        await self.client.send_message(ctx.message.channel ,"database command recieved")
        if ctx.invoked_subcommand is None:
            await self.client.say("incorrect subcommand")
    
    @db.command(pass_context=True)
    async def load(self, ctx):
        if self.conn is None:
            self.conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
            await self.client.send_message(ctx.message.channel ,"Connected")
        else:
            await self.client.say("Already connected")

    @db.command()
    async def unload(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            await self.client.say("Disconnected")








def setup(client):
    client.add_cog(database(client))