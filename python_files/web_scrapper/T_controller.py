import threading
import time

from python_files.structures import Queue
from python_files.database import queries

from .T_worker import Worker


class WorkerController(threading.Thread):
	def __init__(self):
		super().__init__(daemon=True)

		self.queue = Queue()

		self.max_threads = 5
		self.num_threads = 0

		self.busy_ids = []

		self.start()

	def on_manga_done(self, manga):
		self.busy_ids.remove(manga.id)

		self.num_threads -= 1

	def on_chapter_download(self, manga):
		self.queue.append(manga)

	def run(self):
		while True:
			all_manga = queries.get_all_downloadable()

			all_ids_busy = False

			for m in all_manga:
				# TODO: v3.8 This would be a good example of using the walrus operator
				# Wait for free thread
				thread_available = (self.max_threads - self.num_threads) > 0
				while not thread_available:
					thread_available = (self.max_threads - self.num_threads) > 0
					""" Waiting... """
					time.sleep(0.5)

				if m.id in self.busy_ids:
					continue

				all_ids_busy = False

				self.busy_ids.append(m.id)

				self.num_threads += 1

				Worker(m, on_dl_callback=self.on_chapter_download, on_done_callback=self.on_manga_done)
			# -

			if all_ids_busy:
				# If all ID's are being worked on, then take a break
				time.sleep(5)



