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
            "mp3" : "youtube-dl --no-playlist --default-search \"auto\" --audio-quality 0 --extract-audio --audio-format mp3 --embed-thumbnail --add-metadata --postprocessor-args '-movflags faststart' -o ",
            "mp4" : "youtube-dl --no-playlist --default-search \"auto\" -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best' --merge-output-format mp4 --add-metadata --postprocessor-args '-movflags faststart' -o ",
            "mkv" : "youtube-dl --no-playlist --default-search \"auto\" --merge-output-format mkv --add-metadata --postprocessor-args '-movflags faststart' -o "
        }
        
#---------------------------------------------YOUTUBE---------------------------------------------------------------------------------
    @commands.command()
    async def ytdl(self, ctx, *, url: str):
        Cext = "mp3"
        name = random.getrandbits(64)
        modifiers = re.findall('--\w*\s[^ ]*', url)
        for mod in modifiers:
            mod = mod.split(" ")
            if mod[0] == "--f" and mod[1] in self.args.keys():
                Cext = mod[1]
            elif mod[0] == "--n":
                name = mod[1]
        url = re.sub('--\w*\s[^ ]*', '', url)
        to_run = self.args[Cext] + f"\"{name}.%(ext)s\" " + f"\"{url}\""
        embed = discord.Embed(title="Nep is getting your file")
        embed.set_image(url="https://i.kym-cdn.com/photos/images/original/001/283/141/58e.gif")
        embed.set_footer(text=url)
        msg = await ctx.send(embed=embed)
        process = await asyncio.create_subprocess_shell(to_run, stdout=asyncio.subprocess.PIPE)
        await process.communicate()
        with open(f"{name}.{Cext}", "rb") as f:
            resp = await database.sendFile(self, ctx, f)
            if isinstance(resp, str):
                await ctx.send(f"https://www.hitsounds.moe/static/proxyvideo.html#{resp}")
        os.remove(f"{name}.{Cext}")
        await msg.delete()

 


def setup(client):
    discord.opus.load_opus("libopus.so.0")
    if discord.opus.is_loaded():
        print("Opus loaded!")
    client.add_cog(voice(client))
