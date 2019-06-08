
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7.x
"""


def main():
	import os
	import web_scrapper.controller
	import database.alchemy
	import user_interface.windows

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	if database.alchemy.DatabaseFactory.create():

		manga_download_controller = web_scrapper.controller.WebScrapperController()

		user_interface.windows.Application(manga_download_controller).mainloop()


if __name__ == "__main__":
	main()
