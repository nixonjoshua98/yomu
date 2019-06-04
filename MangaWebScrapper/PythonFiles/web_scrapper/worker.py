import os
import threading
import dataclasses
import _functions

from . import manganelo


@dataclasses.dataclass(init=True)
class DownloadQueueRow:
	title: str
	chapter: float


class WebScrapperWorker(threading.Thread):
	def __init__(self, data, queue, completion_callback):
		super().__init__(daemon=True)

		self.data = data
		self.queue = queue
		self.completion_callback = completion_callback

	def run(self):
		chapter_list = manganelo.ChapterList(self.data.url)

		chapter_list.start()

		for c in chapter_list:
			formatted_title = _functions.remove_nasty_chars(self.data.title)

			file_path = _functions.get_chapter_save_location(formatted_title, c.chapter_num)

			os.makedirs(os.path.dirname(file_path), exist_ok=True)

			if not os.path.isfile(file_path):
				download = manganelo.ChapterDownload(c.url, file_path)

				download.start()

				if download.success:
					self.queue.append(DownloadQueueRow(title=formatted_title, chapter=c.chapter_num))

		self.completion_callback(self.data.id)
