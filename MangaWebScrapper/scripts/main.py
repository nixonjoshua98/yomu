
"""
TODO:	Work on thread worker
"""


def main():
	import os
	import time

	from scripts import database as db
	from scripts import workers

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	db.create()

	worker_controller = workers.Controller()

	worker_controller.start()

	time.sleep(60)


if __name__ == '__main__':
	main()