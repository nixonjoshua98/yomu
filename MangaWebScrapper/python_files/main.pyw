
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7.x
"""

"""
data_structures
database
interface_widgets
manga_downloader
static_classes
	data_classes
	enums
	user_data
user_interface
	
main.py
"""


def main():
	import os
	import database

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	database.DatabaseFactory.create_engine()
	database.DatabaseFactory.create_factory()

	import user_interface.windows
	import web_scrapper.controller

	manga_download_controller = web_scrapper.controller.WebScrapperController()
	user_interface.windows.Application(manga_download_controller).mainloop()


if __name__ == "__main__":
	main()
