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
    async def db(self):
        if ctx.invoked_subcommand is None:
            self.client.say("incorrect subcommand")
    
    @db.command()
    async def load(self):
        if self.conn is None:
            self.conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
            self.client.say("Database connection established")
        else:
            self.client.say("Already connected")

    @db.command()
    async def unload(self):
        if self.conn is not None:
            self.conn.close()
            self.client.say("Disconnected")







def setup(client):
    client.add_cog(database(client))