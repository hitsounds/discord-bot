import discord
import youtube_dl
from discord.ext import commands
import aiohttp
import os
import asyncio
from ext.database import database
import random
import functools
import re


class voice:
    def __init__(self, client):
        self.client = client
        self.args = {
            "mp3" : "youtube-dl --no-playlist --default-search \"auto\" --audio-quality 0 --extract-audio --audio-format mp3 --embed-thumbnail --add-metadata -o ",
            "mp4" : "youtube-dl --no-playlist --default-search \"auto\" -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio' --merge-output-format mp4 --add-metadata -o "
        }
        
#---------------------------------------------YOUTUBE---------------------------------------------------------------------------------
    @commands.command()
    async def ytdl(self, ctx, *, url: str):
        Cext = "mp3"
        name = random.getrandbits(64)
        modifiers = re.findall('--[a-zA-Z0-9_]*\s[a-zA-Z0-9_]*', url)
        for mod in modifiers:
            mod = mod.split(" ")
            if mod[0] == "--f" and mod[1] in self.args.keys():
                Cext = mod[1]
            elif mod[0] == "--n":
                name = mod[1]
        url = re.sub('--[a-zA-Z0-9_]*\s[a-zA-Z0-9_]*', '', url)
        to_run = self.args[Cext] + f"\"{name}.%(ext)s\" " + f"\"{url}\""
        embed = discord.Embed(title="Nep is getting your file")
        embed.set_image(url="https://i.kym-cdn.com/photos/images/original/001/283/141/58e.gif")
        embed.set_footer(text=url)
        msg = await ctx.send(embed=embed)
        if Cext == "mp4":
            process = await asyncio.create_subprocess_shell(to_run, stdout=asyncio.subprocess.PIPE)
            await process.communicate()
        elif Cext == "mp3":
            process = await asyncio.create_subprocess_shell(to_run, stdout=asyncio.subprocess.PIPE)
            await process.communicate()
        with open(f"{name}.{Cext}", "rb") as f:
            await database.sendFile(self, ctx, f)
        os.remove(f"{name}.{Cext}")
        await msg.delete()

 


def setup(client):
    discord.opus.load_opus("vendor/lib/libopus.so.0")
    if discord.opus.is_loaded():
        print("Opus loaded!")
    client.add_cog(voice(client))
