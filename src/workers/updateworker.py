import time
import threading

from src import storage
from src.datasources import DataSourceType, AbstractDataSource, ManganeloDataSource


class UpdateWorker(threading.Thread):
	def __init__(self):
		super(UpdateWorker, self).__init__(daemon=True)

	def run(self) -> None:
		storage_instance = storage.get()

		while self.is_alive():
			for status in (0, 1, 2, 3):
				results = storage_instance.get_all_with_status(status)

				for row in results:
					source = self.get_source(DataSourceType.MANGANELO)

					if chapters := source.get_chapters(url=row["url"]):
						latest = max(chapters, key=lambda chap: chap.chapter)

						if latest.chapter != row["latest_chapter"]:
							storage_instance.update_one(row["mangaId"], {"latest_chapter": latest.chapter})

					time.sleep(0.2)

			storage_instance.backup(r"E:\OneDrive\Databases\mongo\Local")

			time.sleep(60)

	@staticmethod
	def get_source(_type) -> AbstractDataSource:
		return {
			DataSourceType.MANGANELO: ManganeloDataSource
		}[_type]
