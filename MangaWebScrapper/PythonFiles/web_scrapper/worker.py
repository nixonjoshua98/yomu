import os
import threading
import dataclasses
import functions
import operator
import enums

import database.queries

from . import manganelo


@dataclasses.dataclass(init=True)
class DownloadQueueRow:
	title: str
	chapter: float


class WebScrapperWorker(threading.Thread):
	def __init__(self, data, queue, completion_callback, website_id=enums.WebsiteEnum.MANGANELO):
		super().__init__(daemon=True)

		self.chapter_list_functions = {
			enums.WebsiteEnum.MANGANELO: manganelo.ChapterList
		}

		self.download_functions = {
			enums.WebsiteEnum.MANGANELO: manganelo.ChapterDownload
		}

		self.download_func = self.download_functions[website_id]
		self.chapter_list_func = self.chapter_list_functions[website_id]

		self.data = data
		self.queue = queue
		self.completion_callback = completion_callback

	def run(self):
		chapter_list = self.chapter_list_func(self.data.url)

		chapter_list.start()

		for c in chapter_list.results:
			formatted_title = functions.remove_nasty_chars(self.data.title)

			file_path = functions.get_chapter_save_location(formatted_title, c.chapter_num)

			os.makedirs(os.path.dirname(file_path), exist_ok=True)

			if not os.path.isfile(file_path):
				download = self.download_func(c.url, file_path)

				download.start()

				if download.success:
					self.queue.append(DownloadQueueRow(title=formatted_title, chapter=c.chapter_num))

		# Update the latest chapter in the database
		if len(chapter_list.results) > 0:
			latest_chapter = max(chapter_list.results, key=operator.attrgetter("chapter_num"))

			# Update the latest chapter (Previously read from directory which is very slow)
			if latest_chapter.chapter_num > self.data.latest_chapter:
				# This occurs twice I think but I cannot figure out why
				database.queries.manga_update_with_id(self.data.id, latest_chapter=latest_chapter.chapter_num)

		self.completion_callback(self.data.id)
