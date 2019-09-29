import threading
import time
import random

from scripts import database as db
from .download_worker import DownloadWorker
from .cleanup_worker import CleanupWorker


class Controller(threading.Thread):
	def __init__(self):
		super(Controller, self).__init__(daemon=True)

		self.ids_processing = set()
		self.max_threads = 1
		self.current_thread_count = 0

	@staticmethod
	def row_generator():
		results = db.select_all_downloadable_manga()

		random.shuffle(results)

		for row in results:
			yield row

	def wait_for_free_thread(self):
		while self.current_thread_count >= self.max_threads:
			time.sleep(0.5)
		return True

	def run(self):
		"""
		Why I didn't use multiprocessing.map - I created the 'wait_for_free_thread' method as I didn't want to spawn
		potentially a tonne of threads which are going to bombard the server all at once. This way I can set a delay
		between each thread being created in the controller, and not the worker. This is more convenient as I may have
		multiple worker classes at some point.
		"""

		while True:
			for row in self.row_generator():

				time.sleep(1.0)

				if row.id in self.ids_processing:
					continue

				self.wait_for_free_thread()

				worker = DownloadWorker(row, lambda: self.on_worker_finish(row))

				worker.start()

				self.current_thread_count += 1
				self.ids_processing.add(row.id)
			# // for row in self.row_generator():

			self.wait_for_free_thread()

			CleanupWorker(db.select_all_manga()).start()
		# // while True:

	def on_worker_finish(self, manga):
		self.current_thread_count -= 1
		self.ids_processing.discard(manga.id)
