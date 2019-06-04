
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7.x
"""


def main():
	import os
	import web_scrapper

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	import user_interface.windows as windows
	import database.database_alchemy as database_alchemy

	if database_alchemy.Database.create():

		manga_download_controller = web_scrapper.WebScrapperController()

		windows.Application(manga_download_controller).mainloop()


if __name__ == "__main__":
	main()
