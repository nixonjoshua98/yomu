import os
import threading


class Worker(threading.Thread):
	def __init__(self, manga, callback):
		super(Worker, self).__init__(daemon=True)

		self.manga = manga
		self.callback = callback

	def run(self):
		print(self.manga)

		self.callback()
