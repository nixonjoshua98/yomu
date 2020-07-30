import time
import random
import threading

from manganelo import MangaInfo


class ChapterWorker(threading.Thread):
	def __init__(self, *, database):
		super(ChapterWorker, self).__init__(daemon=True)

		self.database = database

	def run(self) -> None:
		while True:
			results = self.database.manga.aggregate([{"$match": {"$and": [{"status": {"$lt": 3}}]}}])

			for row in sorted(results, key=lambda _: random.random()):
				info = MangaInfo(row["url"])

				try:
					results = info.results()
				except AttributeError as e:
					print(f"Handled Exception - {e} - ({row['_id']}, {row['status']}, {row['title']}, {row['url']})")
					continue

				latest_chapter = max(results.chapters, key=lambda e: e.num)

				if latest_chapter.num > row["latest_chapter"]:
					self.database.manga.update({"_id": row["_id"]}, {"$set": {"latest_chapter": latest_chapter.num}})

				time.sleep(2.5)
