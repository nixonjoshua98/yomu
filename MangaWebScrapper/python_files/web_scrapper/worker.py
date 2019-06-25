import os
import threading
import functions
import operator

import database.queries

from data_classes import MangaDataClass


class WebScrapperWorker(threading.Thread):
	def __init__(self, data, queue, completion_callback):
		super().__init__(daemon=True)

		self.data = data
		self.queue = queue
		self.completion_callback = completion_callback

	def run(self):
		scrapper_module = functions.url_to_scrapper_module(self.data.url)

		if scrapper_module is None:
			print(self.data.url, "is not a supported url")
			self.completion_callback(self.data.id)
			return

		chapter_list = scrapper_module.ChapterList(self.data.url)

		chapter_list.start()

		for c in chapter_list.results:
			formatted_title = functions.remove_nasty_chars(self.data.title)

			file_path = functions.get_chapter_save_location(formatted_title, c.chapter)

			os.makedirs(os.path.dirname(file_path), exist_ok=True)

			if not os.path.isfile(file_path):
				download = scrapper_module.ChapterDownload(c.url, file_path)

				# download.start()

				if download.success:
					row = MangaDataClass()

					row.title = formatted_title
					row.chapter = c.chapter

					self.queue.append(row)

		# Update the latest chapter in the database
		if len(chapter_list.results) > 0:
			latest_chapter = max(chapter_list.results, key=operator.attrgetter("chapter"))

			# Update the latest chapter (Previously read from directory which is very slow)
			if latest_chapter.chapter > self.data.latest_chapter:
				# This occurs twice I think but I cannot figure out why
				database.queries.manga_update_with_id(self.data.id, latest_chapter=latest_chapter.chapter)

		self.completion_callback(self.data.id)
