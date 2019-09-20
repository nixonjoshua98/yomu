
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7.x
"""

"""
Next Iteration:
- Have UI class with a callback class combined (composition) -> interface_containers & interface_controllers
	- StatusEnum -> Status(int=0, text="Recently Added", downloadable=True) | def text2int, int2text etc.
	- Reduce loose functions -> Static methods when possible
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
