import youtube_dl
import zipfile
import tarfile
import re
import random
import os
import shutil


class ytdl_downloader():
	formats = {
		"mp3": {
			'default_search': 'auto',
			"verbose": True,
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
		self.part = 0
		self.finished = False

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
		base["outtmpl"] = self.path + "/%(id)s.%(ext)s"
		self.ytdlopts = base

	def aio_initalise(self):
		self.extract_info_ytdl()
		self.process_mods()
		self.compile_ytdl_options()

	def dl(self):
		if not self.is_playlist:
		
			with youtube_dl.YoutubeDL(self.ytdlopts) as ydl:
				ydl.download([self.info["webpage_url"]])
			os.rename(self.path + "/{}.{}".format(self.info["id"], self.format), self.path + "/{}.{}".format(self.info["title"], self.format))
			return self.path + "/{}.{}".format(self.info["title"], self.format)
		
		
		elif self.is_playlist and not self.playlist:
			to_dl = self.info["entries"][0]
			with youtube_dl.YoutubeDL(self.ytdlopts) as ydl:
				ydl.download([to_dl["webpage_url"]])
			os.rename(self.path + "/{}.{}".format(to_dl["id"], self.format), self.path + "/{}.{}".format(to_dl["title"], self.format))
			return self.path + "/{}.{}".format(to_dl["title"], self.format)

		elif self.is_playlist and self.playlist:
			try:
				os.remove(f"part_{str(self.part-1)}.zip")
			except Exception:
				pass
			while self.downloaded < len(self.info["entries"]):
				to_dl = self.info["entries"][self.downloaded]
				with youtube_dl.YoutubeDL(self.ytdlopts) as ydl:
					ydl.download([to_dl["webpage_url"]])
				self.downloaded = self.downloaded + 1

				if sum(os.path.getsize(self.path + f) for f in os.listdir(self.path) if os.path.isfile(f)) > 500000000:
					archive = zipfile.ZipFile(self.path + f"part_{str(self.part)}.zip", "w", zipfile.ZIP_DEFLATED)
					for f in os.listdir(self.path):
						archive.write(self.path + f"/{f}", f)
						os.remove(self.path + f"/{f}")
					archive.close()
					self.part = self.part + 1
					return self.path + f"/part_{str(self.part-1)}.zip"

			archive = zipfile.ZipFile(self.path + f"/part_{str(self.part)}.zip", "w", zipfile.ZIP_DEFLATED)
			for f in os.listdir(self.path):	
				archive.write(self.path + f"/{f}", f)
				os.remove(self.path + f"/{f}")
			archive.close()
			self.part = self.part + 1
			self.finished = True
			return self.path + f"/part_{str(self.part-1)}.zip"
				

	def cleanup(self):
		shutil.rmtree(self.path)