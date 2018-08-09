import os
import psycopg2
import discord
from discord.ext import commands

class database:
    def __init__(self, client):
        self.client = client
        self.conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
        self.cur = self.conn.cursor()

    @commands.command()
    async def version(self):
        self.cur.execute("SELECT version()")
        self.client.say(self.cur.fetchone())




def setup(client):
    client.add_cog(database(client))