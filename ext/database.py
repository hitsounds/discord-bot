import os
import psycopg2
import discord
from discord.ext import commands
import re
import aiohttp
from libs.lib import config


class database:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def scan(self, ctx):
        self.conn = await self.load()
        self.cur = self.conn.cursor()
        for member in ctx.message.guild.members:
            self.cur.execute("""INSERT INTO users (user_id, u_name) VALUES ('{userID}', E'{name}') ON CONFLICT (user_id) DO UPDATE SET u_name=E'{name}'""".format(userID = member.id, name = re.escape(member.name)))
            self.conn.commit()
        print("Members in {} registered on database".format(ctx.message.guild))
        await ctx.send("Members in {} registered on database".format(ctx.message.guild))
        self.cur.close()
        self.conn.close()
    
    @classmethod
    async def query(cls, query):
        conn = await cls.load()
        cur = conn.cursor()
        cur.execute(query)
        try:
            resp = cur.fetchall()
        except psycopg2.ProgrammingError:
            resp = None
            pass
        conn.commit()
        cur.close()
        conn.close()
        return resp
        
    @staticmethod
    async def load():
            return psycopg2.connect(config.get("db_url"), sslmode="require")

    async def sendFile(self, ctx ,file):
        if os.fstat(file.fileno()).st_size/1048576. < 7.9:
            return await ctx.send(file=discord.File(file))
        else:
            async with aiohttp.ClientSession() as session:
                resp = await session.post('https://transfer.sh', data={'file': file})
            return await ctx.send(await resp.text())





def setup(client):
    client.add_cog(database(client))
