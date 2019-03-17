import youtube_dl
import zipfile
import tarfile
import re
import random
import os


class ytdl_downloader():
	formats = {
		"mp3": {
			'default_search': 'auto',
			"verbose": True,
			"format": "bestaudio/best",
			"postprocessor_args": ["-movflags", "faststart"],
			"writethumbnail": True,
			"noplaylist": True,
			'postprocessors': [
				{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '0'
				},
				{
					'key': 'EmbedThumbnail'
				},
				{
					'key': "FFmpegMetadata"
				}
			]
		}
	}

	def __init__(self, args):
		self.raw = args
		self.search = re.sub(
			'(?<=\s)-\w*?\s[^ ]*|(?<=\s)--\w*', "", args) or "toaru masterpiece"
		self.mods = re.findall('(?<=\s)-\w*?\s[^ ]*|(?<=\s)--\w*', args)
		self.playlist = False
		self.is_playlist = False
		self.quality = "0"
		self.format = "mp3"  # defaults
		self.downloaded = 0

	def extract_info_ytdl(self):
		with youtube_dl.YoutubeDL({'default_search': 'auto'}) as ydl:
			self.info = ydl.extract_info(self.search, download=False)

	def process_mods(self):
		for i in self.mods:
			if i.startswith("-f") and i.split(" ")[1] in self.formats.keys():
				self.format = i.split(" ")[1]
			elif i.startswith("-q") and 0 <= int(i.split(" ")[1]) <= 350:
				self.quality = i.split(" ")[1]
			elif i.startswith("--pl") and "entries" in self.info:
				self.playlist = True

	def compile_ytdl_options(self):
		base = self.formats[self.format]
		if self.quality != "0" and self.format == "mp3":
			base["postprocessors"][0]["preferredquality"] = self.quality
		if "entries" in self.info:
			self.is_playlist = True
		self.id = str(random.getrandbits(64))
		self.path = f"temp/ytdl/{self.id}"
		base["outtmpl"] = self.path + "/%(title)s.%(ext)s"
		self.ytdlopts = base

	def aio_initalise(self):
		self.extract_info_ytdl()
		self.process_mods()
		self.compile_ytdl_options()

	def dl(self):
		if not self.is_playlist:
			with youtube_dl.YoutubeDL(self.ytdlopts) as ydl:
				ydl.download([self.info["webpage_url"]])
			return os.path.join(self.path, "/{}.{}".format(self.info["title"], self.format))
		elif self.is_playlist and not self.playlist:
			to_dl = self.info["entries"][0]
			with youtube_dl.YoutubeDL(self.ytdlopts) as ydl:
				ydl.download([to_dl["webpage_url"]])
			return os.path.join(self.path, "/{}.{}".format(to_dl["title"], self.format))
