import time
import threading

from src import storage
from src.datasources import AbstractDataSource, ManganeloDataSource, MangaKatanaDataSource


class UpdateWorker(threading.Thread):
	def __init__(self):
		super(UpdateWorker, self).__init__(daemon=True)

	def run(self) -> None:
		storage_instance = storage.get()

		while self.is_alive():
			for status in (0, 1, 2, 3):
				results = storage_instance.get_all_with_status(status)

				for row in results:
					source = self.get_source(row["url"])

					try:
						if not (chapters := source.get_chapters(url=row["url"])):
							continue

					except BaseException as e:
						print(f"{row['title']} | {e}")
						continue

					latest = max(chapters, key=lambda chap: chap.chapter)

					if latest.chapter != row["latest_chapter"]:
						storage_instance.update_one(row["_id"], {"latest_chapter": latest.chapter})

					time.sleep(0.2)

			storage_instance.backup(r"E:\OneDrive\Databases\mongo\Local")

			time.sleep(60)

	@staticmethod
	def get_source(url: str) -> AbstractDataSource:
		if any(map(lambda ele: ele in url, ("manganelo", "manganato"))):
			return ManganeloDataSource

		return MangaKatanaDataSource
