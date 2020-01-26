import threading
import time
import random

from .worker import WebScrapperWorker

from python_files.structures import Queue
from python_files.common import manga_status
from python_files.database import queries as database_queries


def database_generator(status_list):
	while True:
		data = database_queries.manga_select_all_in_status_list(status_list)

		random.shuffle(data)

		for c in data:
			yield c


class WebScrapperController(threading.Thread):
	def __init__(self):
		super().__init__(daemon=True)

		self.queue = Queue()

		self.total_threads = 0
		self.max_threads = 1

		self.ids_downloading = []

		self.start()

	def run(self):
		# manga_status.all_downloadable_ids()
		data_gen = database_generator((0,))

		while True:
			time.sleep(0.5)

			is_thread_available = self.max_threads - self.total_threads >= 1

			if is_thread_available:
				next_data = next(data_gen)

				if next_data.id in self.ids_downloading:
					continue

				# Create new worker
				self.ids_downloading.append(next_data.id)
				self.total_threads += 1

				thread = WebScrapperWorker(next_data, self.queue, self.worker_completion_callback)

				thread.start()

	def worker_completion_callback(self, data_id):
		self.total_threads -= 1
		self.ids_downloading.remove(data_id)
