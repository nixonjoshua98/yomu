
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7
"""

# TODO: Interface


def main():
	import os
	import sys

	sys.path.append(os.path.dirname(os.path.dirname(__file__)))

	from python_files import database
	from python_files.user_interface.windows import Application
	from python_files.web_scrapper import WorkerController

	database.init()

	controller = WorkerController()

	app = Application(controller)

	app.mainloop()


if __name__ == "__main__":
	main()
