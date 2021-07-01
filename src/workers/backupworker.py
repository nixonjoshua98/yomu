
import time
import threading

from src import storage


class BackupWorker(threading.Thread):
	def __init__(self):
		super(BackupWorker, self).__init__(daemon=True)

	def run(self) -> None:
		while True:
			storage.get_instance().backup(r"E:\OneDrive\Databases\mongo\Local")

			time.sleep(60)
