import threading


def run_in_pool(func, callback):

	def _run_in_pool():
		callback(func())

	(_ := threading.Thread(target=_run_in_pool)).start()
