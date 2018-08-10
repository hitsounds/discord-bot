import discord
from discord.ext import commands
import random
import praw
import os

class fun:
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id=os.environ.get('C_ID'),
                     client_secret=os.environ.get('C_S'),
                     user_agent='bot.py A discord bot')


    
    @commands.group(pass_context=True)
    async def bws(self, ctx):
        if ctx.invoked_subcommand is None:
            self.bwl = self.reddit.subreddit('awwnime').hot()
            self.post_to_pick = random.randint(1, 10)
            for i in range(0, self.post_to_pick):
                self.submission = next(x for x in self.bwl if not x.stickied)
            await self.client.send_message(ctx.message.channel ,self.submission.url)
    
    @bws.command(pass_context=True)
    async def dump(self, ctx):
        self.sreddit = self.reddit.subreddit('awwnime')
        self.bwl = self.reddit.subreddit('awwnime').hot()
        self.embed=discord.Embed(title="Current bws selection", url="https://www.reddit.com/r/awwnime/hot/")
        self.embed.set_author(name="Source", url="https://www.reddit.com/r/awwnime/", icon_url=self.sreddit.icon_img)
        self.embed.set_thumbnail(url="https://cdn.awwni.me/13dgm.png")
        for i in range(0, 10):
            self.embed.add_field(name="#{}".format(i+1), value="[{url}]({url})".format(url = next(x for x in self.bwl if not x.stickied).url), inline=False)
        await self.client.say(embed=self.embed)
#            await self.client.send_message(ctx.message.channel ,next(x for x in self.bwl if not x.stickied).url)
        





    @commands.command()
    async def ping(self):
        await self.client.say("Pong!")




def setup(client):
    client.add_cog(fun(client))