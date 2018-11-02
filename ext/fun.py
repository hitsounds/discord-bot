import discord
from discord.ext import commands
import random
import praw
import os
import aiohttp
import psycopg2
from ext.database import database
from libs.lib import ImageProcessing
import asyncio
import io
from PIL import Image, ImageFont, ImageDraw, ImageOps

ping_formats = {
    "table_tennis_1.jpg": {"rq_size" : 64, "x" : 250, "y" : 150},
    "table_tennis_2.jpg": {"rq_size" : 64, "x" : 280, "y" : 150},
    "table_tennis_3.jpg": {"rq_size" : 64, "x" : 468, "y" : 295}
}

class fun:
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id=os.environ.get('C_ID'), client_secret=os.environ.get('C_S'), user_agent='bot.py A discord bot | https://github.com/Hitsounds/discord-bot')


    @commands.command(name='anime', aliases=['manga'])
    async def kitsu_search(self, ctx, *, search: str):
        async with ctx.message.channel.typing():
            search = search.replace(" ","%20")
            async with aiohttp.ClientSession() as session:
                resp = await session.get(f"https://kitsu.io/api/edge/{ctx.invoked_with}?filter[text]={search}&page[limit]=1")
                resp = await resp.json()
                resp = resp["data"][0]["attributes"]
            embed=discord.Embed(title="Rating: {}%".format(resp["averageRating"]), description=resp["synopsis"], color=0x4d30d6)
            embed.set_author(name="{} ({})".format(resp["canonicalTitle"],resp["subtype"]), url="https://kitsu.io/anime/{}".format(resp["slug"]))
            embed.set_thumbnail(url=resp["posterImage"]["original"])
            embed.add_field(name="Start", value=resp["startDate"], inline=True)
            embed.add_field(name="End", value=resp["endDate"], inline=True)
            embed.add_field(name="Status", value=resp["status"], inline=True)
            embed.add_field(name="Next Release", value=resp["nextRelease"], inline=True)
            embed.set_footer(text=resp["ageRatingGuide"])
            await ctx.send(embed=embed)


    @commands.group()
    async def bws(self, ctx):
        if ctx.invoked_subcommand is None:
            bwl = self.reddit.subreddit('awwnime').hot()
            for i in range(0,random.randint(1, 10)):
                submission = next(x for x in bwl if not x.stickied)
            await ctx.send(submission.url)


    @bws.command()
    async def dump(self, ctx):
        sreddit = self.reddit.subreddit('awwnime')
        bwl = self.reddit.subreddit('awwnime').hot()
        embed=discord.Embed(title="Current bws selection", url="https://www.reddit.com/r/awwnime/hot/")
        embed.set_author(name="Source", url="https://www.reddit.com/r/awwnime/", icon_url=sreddit.icon_img)
        embed.set_thumbnail(url="https://cdn.awwni.me/13dgm.png")
        for i in range(0, 10):
            embed.add_field(name="#{}".format(i+1), value="[{url}]({url})".format(url = next(x for x in bwl if not x.stickied).url), inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def yomama(self, ctx):
        await ctx.message.delete()
        async with aiohttp.ClientSession() as session:
            resp = await session.get("http://api.yomomma.info/")
        data = await resp.json()
        await ctx.send(data["joke"])


    @commands.command()
    async def banter(self, ctx):
        async with aiohttp.ClientSession() as session:
            resp = await session.get("https://docs.google.com/document/export?format=txt&id=11-TyNEPW-VWMxqqY4UdJJLM0JgD5kagntURBUD6EbZw")
            lol = await resp.text()
        embed=discord.Embed(title="OwO", description=random.choice(lol.split("\n")), color=0x0a94e7)
        embed.set_footer(text = "Credit to George's dead banter bot", icon_url = "https://cdn.discordapp.com/avatars/478220076068241408/8560a1bedb1432d1cdf8dcf634ac3a4d.png")
        await ctx.send(embed=embed)       


    @commands.command(name='ping', aliases=['pang',"pong","pung"])
    async def ping_(self, ctx):
        template = random.choice(list(ping_formats))
        tempdDetails = ping_formats[template]
        size = (tempdDetails["rq_size"], tempdDetails["rq_size"])
        uimg = await ImageProcessing.PIL_image_from_url(ctx.message.author.avatar_url_as(static_format="png", size=tempdDetails["rq_size"]))
        background = Image.open(f"assets/ping/{template}")
        mask = Image.new('L', size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + size, fill=255)
        background.paste(uimg, (tempdDetails["x"], tempdDetails["y"]), mask)
        background.save(f"ping_out_{ctx.message.author.name}.png")
        with open(f"ping_out_{ctx.message.author.name}.png", "rb") as f:
            await database.sendFile(self, ctx, f)
        os.remove(f"ping_out_{ctx.message.author.name}.png")











def setup(client):
    client.add_cog(fun(client))
