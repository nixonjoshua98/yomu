
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7.x
"""


def get_old_database():
	import sqlite3
	from database.database_queries import manga_insert_row

	with sqlite3.connect(r"D:\OneDrive - UoL\OneDrive - University of Lincoln\DB.DB") as db:
		cursor = db.cursor()
		cursor.execute("SELECT * FROM COMICS")
		rows = cursor.fetchall()

	for i, r in enumerate(rows):
		manga_insert_row(title=r[1], url=r[2], chapters_read=r[4], status=r[5])


if __name__ == "__main__":
	import user_interface.windows as windows
	import database.database_alchemy as database_alchemy
	import controllers.manga_download_controller as manga_download_controller

	database_alchemy.Database.create()

	download_controller = manga_download_controller.MangaDownloadController()

	# get_old_database()

	# Mainloop blocks the main execution so things under od not run yet
	windows.Application(download_controller).mainloop()

	download_controller.running = False
