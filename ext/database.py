import os
import psycopg2
import discord
from discord.ext import commands

class database:
    def __init__(self, client):
        self.client = client
        self.conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")

    @commands.command()
    async def tablec(self):
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE users(user_id bigint PRIMARY KEY, user_name varchar(35));")
        self.conn.commit()
        print ("Users table created :D")
        self.cur.close()





def setup(client):
    client.add_cog(database(client))