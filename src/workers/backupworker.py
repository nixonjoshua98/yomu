import os
import json
import time
import threading

import datetime as dt


BACKUP_PATH = "D:\\Program Files\\OneDrive\\Databases\\mongo\\manga"


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

			now = dt.datetime.now().strftime("%y-%m-%d %H-%M-%S")

			with open(os.path.join(BACKUP_PATH, f"{now}.json"), "w") as fh:
				json.dump(data, fh)

			time.sleep(300)
