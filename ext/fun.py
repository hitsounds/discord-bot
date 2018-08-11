import discord
from discord.ext import commands
import random
import praw
import os
import aiohttp

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


    @commands.group(pass_context=True)
    async def osu(self, ctx, arg):
        if ctx.invoked_subcommand is None:
            session = aiohttp.ClientSession()
            resp = await session.get("https://osu.ppy.sh/api/get_user?k={self.osuAPIkey}&u={arg}&m=0")
            await client.say(resp.json())    

            




        





    @commands.command()
    async def ping(self):
        await self.client.say("Pong!")




def setup(client):
    client.add_cog(fun(client))