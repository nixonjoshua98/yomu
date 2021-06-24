
import time
import subprocess
import threading


class BackupWorker(threading.Thread):
	def __init__(self, *, database):
		super(BackupWorker, self).__init__(daemon=True)

		self.database = database

	def run(self) -> None:
		while True:
			path = r"E:\OneDrive\Databases\mongo\Local"

			cmd = f'mongodump.exe -d {self.database.name} -o "{path}"'

			subprocess.run(cmd)

			time.sleep(60)