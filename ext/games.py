import discord
from discord.ext import commands
import random
import os
import aiohttp
import psycopg2
from ext.database import database
from libs.lib import ImageProcessing
import asyncio
from PIL import Image, ImageFont, ImageDraw, ImageOps

class osu:
    def __init__(self, client):
        self.client = client
        self.osuAPIkey = os.environ.get('OSU_KEY')

    async def save_osuID(self, ctx, args):
        if len(args) < 2:
                await ctx.send("Pass a osu! user name or id with the command.\n ```;osu set hitsounds```", delete_after=10.0)
            else:
                async with aiohttp.ClientSession() as session:
                    dtls = await session.get("https://osu.ppy.sh/api/get_user?k={key}&u={name}&m=0".format(key = self.osuAPIkey, name = args[1]))
                dtls = await dtls.json()
                await database.query("""UPDATE users SET osu_id='{osuid}' WHERE user_id={userID}""".format(userID = ctx.message.author.id, osuid = dtls[0]["user_id"]))
                await ctx.send("Osu! linked", delete_after=5.0)

    async def send_osuStats(self, ctx, args):
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            if len(args) == 0:
                arg = await database.query(f"SELECT osu_id FROM users WHERE user_id={ctx.message.author.id}")
                args = arg[0]
            dtls = await session.get("https://osu.ppy.sh/api/get_user?k={key}&u={name}&m=0".format(key = self.osuAPIkey, name = args[0]))
        dtls = await dtls.json()
        dtls = dtls[0]
        embed=discord.Embed(title="Osu Stats" ,description="[Profile](https://osu.ppy.sh/u/{id}) | [PP+](https://syrin.me/pp+/u/{id}/) | [Skills](http://osuskills.tk/user/{name}) | [Osu!-chan](https://syrin.me/osuchan/u/{id}/?m=0) | [Osu!Track](https://ameobea.me/osutrack/user/{name})".format(name = dtls["username"],id = dtls["user_id"]), color=0xdc98a4)
        embed.set_author(name="{} [{}]".format(dtls["username"], dtls["country"] ), url="https://osu.ppy.sh/u/{}".format(dtls["user_id"]), icon_url="https://a.ppy.sh/{}".format(dtls["user_id"]))
        embed.set_thumbnail(url=r"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Osu%21Logo_%282015%29.png/220px-Osu%21Logo_%282015%29.png")
        embed.add_field(name="PP", value=dtls["pp_raw"], inline=True)
        embed.add_field(name="Accuracy", value=str(round(float(dtls["accuracy"]),2))+"%", inline=True)
        embed.add_field(name="Level", value=dtls["level"], inline=True)
        embed.add_field(name="Playcount", value=dtls["playcount"], inline=True)
        embed.add_field(name="Global Rank", value="#" + dtls["pp_rank"], inline=True)
        embed.add_field(name=dtls["country"]+" Rank", value="#"+ dtls["pp_country_rank"], inline=True)
        await ctx.send(embed=embed)


    @commands.command()
    async def osu(self, ctx, *args):
        if args[0] == "set":
            await self.save_osuID(ctx, args)
        else:
            await self.send_osuStats(ctx, args)

def setup(client):
    client.add_cog(osu(client))