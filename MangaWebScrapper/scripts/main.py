
"""
TODO:	Work on thread worker
"""


def main():
	import os
	import time

	from scripts import database as db
	from scripts import thread_workers

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	db.create()

	print("DB Rows:", len(db.select_all_manga()))

	thread_controller = thread_workers.Controller()

	thread_controller.start()


if __name__ == '__main__':
	main()