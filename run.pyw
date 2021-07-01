from pymongo import MongoClient

from src.workers import ChapterWorker, BackupWorker

from src.windows.application import Application


if __name__ == "__main__":

	with MongoClient() as client:
		ChapterWorker().start()
		BackupWorker().start()

		Application().mainloop()
