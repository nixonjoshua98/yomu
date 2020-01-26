
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7
"""

# TODO: Re-write this entire program.


def main():
	import os

	from python_files import database
	from python_files.user_interface.windows import Application
	from python_files.web_scrapper import WorkerController

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	database.init()

	controller = WorkerController()

	app = Application(controller)

	app.mainloop()


if __name__ == "__main__":
	main()
