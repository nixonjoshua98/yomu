import threading
import os

from python_files.manganelo import (ChapterList, ChapterDownload)
from python_files.database import queries
from python_files.common import functions


class Worker(threading.Thread):
	def __init__(self, manga, *, on_dl_callback, on_done_callback):
		super().__init__(daemon=False)

		self.manga = manga
		self.on_dl_callback = on_dl_callback
		self.on_done_callback = on_done_callback

		self.start()

	def run(self):
		chap_ls = ChapterList(self.manga.url, start=True)

		clean_title = functions.remove_nasty_chars(self.manga.title)

		for c in chap_ls.results:
			if c.chapter <= self.manga.chapters_read:
				continue

			chapter_dst = functions.get_manga_save_dir(clean_title, c.chapter)

			if os.path.isfile(chapter_dst):
				continue

			# Create the base directory
			os.makedirs(os.path.dirname(chapter_dst), exist_ok=True)

			# Start the download
			dwn = ChapterDownload(c.url, chapter_dst, start=True)

			if dwn.success:
				self.on_dl_callback([self.manga.title, c.chapter])

		if len(chap_ls.results) == 0:
			print(f"Warning: {self.manga.id} {self.manga.title} {self.manga.url} expired")

		else:
			latest_online_chap = chap_ls.results[-1].chapter
			latest_read_chap = self.manga.latest_chapter

			if latest_online_chap != latest_read_chap:
				queries.update_latest_chapter(_id=self.manga.id, chapter=latest_online_chap)

		self.on_done_callback(self.manga)
