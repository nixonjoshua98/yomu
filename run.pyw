from pymongo import MongoClient

from src.updateworker import UpdateWorker

from src.application import Application

if __name__ == "__main__":
	from src import storage

	x = storage.get().all()

	#storage.get().set_(x)

	with MongoClient() as client:
		app = Application()

		UpdateWorker(app.data_storage).start()

		app.mainloop()
