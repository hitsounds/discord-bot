import discord
from discord.ext import commands
import random
import praw
import os
import aiohttp
import psycopg2
from ext.database import database

class fun:
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id=os.environ.get('C_ID'),
                     client_secret=os.environ.get('C_S'),
                     user_agent='bot.py A discord bot')
        self.osuAPIkey = os.environ.get('OSU_KEY')


    @commands.group(pass_context=True)
    async def bws(self, ctx):
        if ctx.invoked_subcommand is None:
            bwl = self.reddit.subreddit('awwnime').hot()
            post_to_pick = random.randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(x for x in bwl if not x.stickied)
            await self.client.send_message(ctx.message.channel ,submission.url)
            bwl, post_to_pick, submission = None, None, None
    
    @bws.command(pass_context=True)
    async def dump(self, ctx):
        sreddit = self.reddit.subreddit('awwnime')
        bwl = self.reddit.subreddit('awwnime').hot()
        embed=discord.Embed(title="Current bws selection", url="https://www.reddit.com/r/awwnime/hot/")
        embed.set_author(name="Source", url="https://www.reddit.com/r/awwnime/", icon_url=sreddit.icon_img)
        embed.set_thumbnail(url="https://cdn.awwni.me/13dgm.png")
        for i in range(0, 10):
            embed.add_field(name="#{}".format(i+1), value="[{url}]({url})".format(url = next(x for x in bwl if not x.stickied).url), inline=False)
        await self.client.say(embed=embed)
        embed, sreddit, bwl = None, None, None
    
    @commands.command(pass_context=True)
    async def yomama(self, ctx):
        await self.client.delete_message(ctx.message)
        session = aiohttp.ClientSession()
        resp = await session.get("http://api.yomomma.info/")
        session.close()
        data = await resp.json()
        await self.client.say(data["joke"])
        session, resp, data = None, None, None





    @commands.group(pass_context=True)
    async def osu(self, ctx, arg=None):
        if ctx.invoked_subcommand is None:
            msg = await self.client.say("Processing")
            session = aiohttp.ClientSession()
            if arg == None:
                conn = await database.load()
                cur = conn.cursor()
                cur.execute(f"SELECT osu_id FROM users WHERE user_id={ctx.message.author.id}")
                arg = cur.fetchone()
                dtls = await session.get("https://osu.ppy.sh/api/get_user?k={key}&u={name}&m=0".format(key = self.osuAPIkey, name = arg[0]))
                cur.close()
                conn.close()
            else: 
                dtls = await session.get("https://osu.ppy.sh/api/get_user?k={key}&u={name}&m=0".format(key = self.osuAPIkey, name = arg))
            session.close()
            dtls = await dtls.json()
            dtls = dtls[0]
            embed=discord.Embed(title="Osu Stats" ,description="[Profile](https://osu.ppy.sh/u/{id}) | [PP+](https://syrin.me/pp+/u/{id}/) | [Skills](http://osuskills.tk/user/{name}) | [Osu!-chan](https://syrin.me/osuchan/u/{id}/?m=0) | [Osu!Track](https://ameobea.me/osutrack/user/{name})".format(name = dtls["username"],id = dtls["user_id"]), color=0xdc98a4)
            embed.set_author(name="{} [{}]".format(dtls["username"], dtls["country"] ), url="https://osu.ppy.sh/u/{}".format(dtls["user_id"]), icon_url="https://a.ppy.sh/{}".format(dtls["user_id"]))
            embed.set_thumbnail(url=r"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Osu%21Logo_%282015%29.png/220px-Osu%21Logo_%282015%29.png")
            embed.add_field(name="PP", value=dtls["pp_raw"], inline=True)#
            embed.add_field(name="Accuracy", value=str(round(float(dtls["accuracy"]),2))+"%", inline=True)
            embed.add_field(name="Level", value=dtls["level"], inline=True)
            embed.add_field(name="Playcount", value=dtls["playcount"], inline=True)
            embed.add_field(name="Global Rank", value="#" + dtls["pp_rank"], inline=True)
            embed.add_field(name=dtls["country"]+" Rank", value="#"+ dtls["pp_country_rank"], inline=True)
            await self.client.edit_message(msg,new_content="Done!" ,embed=embed)
            embed, dtls, session, msg = None,None,None,None

            








    @commands.command()
    async def ping(self):
        await self.client.say("Pong!")




def setup(client):
    client.add_cog(fun(client))
