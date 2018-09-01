import discord
from discord.ext import commands
import random
import praw
import os
import aiohttp
import psycopg2
from ext.database import database
import asyncio

class fun:
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id=os.environ.get('C_ID'), client_secret=os.environ.get('C_S'), user_agent='bot.py A discord bot | https://github.com/Hitsounds/discord-bot')
        self.osuAPIkey = os.environ.get('OSU_KEY')
        self.session = aiohttp.ClientSession()
        
        

    @commands.group(pass_context=True)
    async def bws(self, ctx):
        if ctx.invoked_subcommand is None:
            bwl = self.reddit.subreddit('awwnime').hot()
            post_to_pick = random.randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(x for x in bwl if not x.stickied)
            await self.client.send_message(ctx.message.channel ,submission.url)
    
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
    
    @commands.command(pass_context=True)
    async def yomama(self, ctx):
        await self.client.delete_message(ctx.message)
        resp = await self.session.get("http://api.yomomma.info/")
        data = await resp.json()
        await self.client.say(data["joke"])

    @commands.command(pass_context=True)
    async def banter(self, ctx):
        if ctx.invoked_subcommand is None:
            resp = await self.session.get("https://docs.google.com/document/export?format=txt&id=1nzdBhs6K1aWP5VpQlcCOX7do-9ZxoCoCPMSWCtXG6m4")
            lol = await resp.text()
            jk = random.choice(lol.split("\n"))
            embed=discord.Embed(title="OwO", description=jk, color=0x0a94e7)
            embed.set_footer(text = "Credit to George's dead banter bot", icon_url = "https://cdn.discordapp.com/avatars/478220076068241408/8560a1bedb1432d1cdf8dcf634ac3a4d.png")
            await self.client.say(embed=embed)



    




    @commands.command(pass_context=True)
    async def osu(self, ctx, *args):
        if len(args)>0 and args[0] == "set":
            """
            Set osu name
            
            """
            if len(args) < 2:
                msg = await self.client.say("Pass a osu! user name or id with the command")
                asyncio.sleep(2)
            else:
                dtls = await self.session.get("https://osu.ppy.sh/api/get_user?k={key}&u={name}&m=0".format(key = self.osuAPIkey, name = args[1]))
                dtls = await dtls.json()
                conn = await database.load()
                cur = conn.cursor()
                cur.execute("""UPDATE users SET osu_id='{osuid}' WHERE user_id={userID}""".format(userID = ctx.message.author.id, osuid = dtls[0]["user_id"]))
                conn.commit()
                cur.close()
                conn.close()
                msg = await self.client.say("Osu! registered")
                asyncio.sleep(2)
                await self.client.delete_message(msg)
                await self.client.delete_message(ctx.message)      
        else:
            """
            
            Get osu stats
            
            """
            await self.client.send_typing(ctx.message.channel)
            if len(args) == 0:
                conn = await database.load()
                cur = conn.cursor()
                cur.execute(f"SELECT osu_id FROM users WHERE user_id={ctx.message.author.id}")
                arg = cur.fetchone()
                dtls = await self.session.get("https://osu.ppy.sh/api/get_user?k={key}&u={name}&m=0".format(key = self.osuAPIkey, name = arg[0]))
                cur.close()
                conn.close()
            else: 
                dtls = await self.session.get("https://osu.ppy.sh/api/get_user?k={key}&u={name}&m=0".format(key = self.osuAPIkey, name = args[0]))
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
            await self.client.say(embed=embed)



            








    @commands.command()
    async def ping(self):
        await self.client.say("Pong!")




def setup(client):
    client.add_cog(fun(client))
