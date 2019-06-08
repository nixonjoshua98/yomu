
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7.x
"""


def main():
	import os
	import web_scrapper
	import database.alchemy
	import user_interface.windows

	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	if database.alchemy.DatabaseFactory.create():

		manga_download_controller = web_scrapper.WebScrapperController()

		user_interface.windows.Application(manga_download_controller).mainloop()


if __name__ == "__main__":
	main()

	import web_scrapper

	ls = web_scrapper.ciayo.ChapterList("https://www.ciayo.com/en/comic/radiative")

	ls.start()

	print(ls.results)
