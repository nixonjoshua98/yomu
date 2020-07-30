import os
import json
import time
import threading


BACKUP_PATH = "D:\\Program Files\\OneDrive\\Databases"


class BackupWorker(threading.Thread):
	def __init__(self, *, database):
		super(BackupWorker, self).__init__(daemon=True)

		self.database = database

	def run(self) -> None:
		while True:
			data = {}

			for collection in self.database.collection_names():
				collection_data = tuple(self.database[collection].find({}, {"_id": 0}))

				data[collection] = collection_data

			os.makedirs(BACKUP_PATH, exist_ok=True)

			with open(os.path.join(BACKUP_PATH, "mongo_manga.json"), "w") as fh:
				json.dump(data, fh)

			time.sleep(300)
