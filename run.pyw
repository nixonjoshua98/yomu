from pymongo import MongoClient

from src.updateworker import UpdateWorker

from src.application import Application

if __name__ == "__main__":

	with MongoClient() as client:
		UpdateWorker().start()

		Application().mainloop()
