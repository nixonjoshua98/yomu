import threading

from scripts.scrappers import manganelo


class DownloadWorker(threading.Thread):
	def __init__(self, manga, callback):
		super(DownloadWorker, self).__init__(daemon=True)

		self.manga = manga
		self.callback = callback

	def run(self):
		chapter_list = manganelo.ChapterList(self.manga.url, start=True)

		latest_chapter = -1

		for i, row in enumerate(chapter_list.results()):
			latest_chapter = max(latest_chapter, row.chapter_num)

			# Ignore the ones which I have already read
			if row.chapter_num < self.manga.chapters_read:
				continue

		self.callback(self.manga)
