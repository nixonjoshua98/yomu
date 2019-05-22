
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7.x
"""

def main():
	import os

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	import user_interface.windows as windows
	import database.database_alchemy as database_alchemy
	import controllers.manga_download_controller as manga_download_controller

	database_alchemy.Database.create()

	download_controller = manga_download_controller.MangaDownloadController()

	# Mainloop blocks the main execution so things under od not run yet
	windows.Application(download_controller).mainloop()

	download_controller.running = False


if __name__ == "__main__":
	main()
