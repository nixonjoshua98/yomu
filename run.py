from pymongo import MongoClient

from src.workers import ChapterWorker, BackupWorker

from src.interface.application import Application


if __name__ == "__main__":
	client = MongoClient("mongodb://localhost:27017/")

	worker = ChapterWorker(database=client.manga)
	backup = BackupWorker(database=client.manga)

	app = Application(database=client.manga, worker=worker)

	worker.start()
	backup.start()

	app.mainloop()

	client.close()
