import time
import threading

import manganelo.rewrite as manganelo


class ChapterWorker(threading.Thread):
	def __init__(self, *, mongo):
		super(ChapterWorker, self).__init__(daemon=True)

		self.mongo = mongo

	def run(self) -> None:
		while self.is_alive():
			results = list(self.mongo.manga.find({"status": {"$lt": 3}}))

			for row in results:
				try:
					page = manganelo.manga_page(url=row["url"])
				except manganelo.NotFound as e:
					print(f"Ignoring Exception: {e}")
					continue

				chapters = page.chapter_list()

				latest = max(chapters, key=lambda chap: chap.chapter)

				if latest.chapter > row["latest_chapter"]:
					self.mongo["manga"].update_one({"_id": row["_id"]}, {"$set": {"latest_chapter": latest.chapter}})

				time.sleep(0.2)

			time.sleep(300)
