import os
import threading
import data_classes
import functions
import operator

import database.queries

from . import enum2module


class WebScrapperWorker(threading.Thread):
	def __init__(self, data, queue, completion_callback):
		super().__init__(daemon=True)

		self.data = data
		self.queue = queue
		self.completion_callback = completion_callback

	def run(self):
		scrapper_module = enum2module.str2module(self.data.url)

		chapter_list = scrapper_module.ChapterList(self.data.url)

		chapter_list.start()

		print("Gotten chapters")

		for c in reversed(chapter_list.results):
			print(c.chapter_num)

			formatted_title = functions.remove_nasty_chars(self.data.title)

			file_path = functions.get_chapter_save_location(formatted_title, c.chapter_num)

			os.makedirs(os.path.dirname(file_path), exist_ok=True)

			if not os.path.isfile(file_path):
				download = scrapper_module.ChapterDownload(c.url, file_path)

				download.start()

				if download.success:
					self.queue.append(data_classes.DownloadQueueRow(title=formatted_title, chapter=c.chapter_num))

		# Update the latest chapter in the database
		if len(chapter_list.results) > 0:
			latest_chapter = max(chapter_list.results, key=operator.attrgetter("chapter_num"))

			# Update the latest chapter (Previously read from directory which is very slow)
			if latest_chapter.chapter_num > self.data.latest_chapter:
				# This occurs twice I think but I cannot figure out why
				database.queries.manga_update_with_id(self.data.id, latest_chapter=latest_chapter.chapter_num)

		self.completion_callback(self.data.id)
