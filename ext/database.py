import os
import psycopg2
import discord
from discord.ext import commands
import re
import aiohttp


class database:
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()

    @commands.command()
    async def scan(self, ctx):
        self.conn = await self.load()
        self.cur = self.conn.cursor()
        for member in ctx.message.guild.members:
            self.cur.execute("""UPDATE users SET u_name=E'{name}' WHERE user_id={userID}""".format(userID = member.id, name = re.escape(member.name)))
            self.conn.commit()
        print("Members in {} registered on database".format(ctx.message.guild))
        self.cur.close()
        self.conn.close()
    


    async def load():
            return psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")

    async def sendFile(self, ctx ,filename ,extension):
        file = f"{filename}.{extension}"
        if os.path.getsize(file)/1048576 < 7:
            res = await ctx.send(file=discord.File(file))
            return res
        else:
            upload = open(file, "rb")
            files = {'filedata': upload}
            resp = await self.session.post('https://transfer.sh/', data=files)
            upload.close()
            res = await ctx.send(await resp.text())
            return res





def setup(client):
    client.add_cog(database(client))
