
"""
Author: Joshua Nixon
Email: nixonjoshua98@gmail.com
Py Version: 3.7.2
Sublime Text 3
"""

def get_old_database():
	import sqlite3
	from database.database_queries import manga_insert_row

	with sqlite3.connect(r"C:\Users\Joshua\OneDrive - University of Lincoln\DB.DB") as db:
		cursor = db.cursor()
		cursor.execute("SELECT * FROM COMICS")
		rows = cursor.fetchall()

	for i, r in enumerate(rows):
		manga_insert_row(title=r[1],
			menu_url=r[2],
			chapters_read=r[4],
			status=r[5],
			)


if __name__ == "__main__":
	import user_interface.windows as windows
	from database.database_alchemy import Database

	Database.create()

	windows.Application().mainloop()
