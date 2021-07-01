import time
import threading

import manganelo.rewrite as manganelo

from src import storage


class ChapterWorker(threading.Thread):
	def __init__(self):
		super(ChapterWorker, self).__init__(daemon=True)

	def run(self) -> None:
		storage_instance = storage.get_instance()

		while self.is_alive():
			for status in (0, 1, 2):
				results = storage_instance.get_with_status(status)

				for row in results:
					try:
						page = manganelo.manga_page(url=row["url"])

					except manganelo.NotFound:
						continue

					chapters = page.chapter_list()

					latest = max(chapters, key=lambda chap: chap.chapter)

					if latest.chapter != row["latest_chapter"]:
						storage_instance.update_one(row["_id"], {"latest_chapter": latest.chapter})

					time.sleep(0.2)

			time.sleep(60)
