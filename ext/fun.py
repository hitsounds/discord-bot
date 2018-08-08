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


    
    @commands.command(pass_context=True)
    async def bws(self, ctx):
        self.bwl = memes_submissions = self.reddit.subreddit('awwnime').hot()
        self.post_to_pick = random.randint(1, 10)
        for i in range(0, self.post_to_pick):
            self.submission = next(x for x in self.bwl if not x.stickied)
        await bot.send_message(ctx.message.channel ,self.submission.url)



            
#        await self.client.send_message(ctx.message.channel, self.bw(random.randint(1,5500)))

    @commands.command()
    async def ping():
        await self.client.say("Pong!")


def setup(client):
    client.add_cog(fun(client))