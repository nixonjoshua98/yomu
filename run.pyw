from pymongo import MongoClient

from src.workers import UpdateWorker

from src.windows.application import Application


if __name__ == "__main__":

	with MongoClient() as client:
		UpdateWorker().start()

		Application().mainloop()
