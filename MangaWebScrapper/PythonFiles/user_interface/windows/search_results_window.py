import tkinter as tk

from tkinter import messagebox

import user_interface.widgets as widgets

import database.database_queries as database_queries


class SearchResultsWindow(widgets.ChildWindow):
	def __init__(self, search_results: dict, headers: tuple, callback):
		super().__init__(f"Search Results ({len(search_results)} results)", destroy_on_exit=True)

		self.callback = callback

		table_callbacks = {
			"Button-3": self.add_manga_to_database
		}

		# - Frames
		table_frame = tk.Frame(self)

		# - Widgets
		table = widgets.Treeview(table_frame, headers, binds=table_callbacks)

		# - Placements
		table_frame.pack(expand=True, fill=tk.BOTH)
		table.pack(expand=True, fill=tk.BOTH)

		table.populate(list(map(lambda r: list(r.values()), search_results)))

	def add_manga_to_database(self, event=None):
		row = event.widget.one()

		if row is not None:
			data = {"title": row[0], "url": row[2]}

			# Check if already in database
			if database_queries.manga_select_one_with_title(data["title"]):
				messagebox.showinfo(data["title"], "Row with the same title already exists in the database")

			else:
				if not messagebox.askyesno("Database", f"Are you sure you want to add '{data['title']}'"):
					return

				if database_queries.manga_insert_row(**data):
					messagebox.showinfo("Database", data["title"] + " has been added")

					self.destroy()

					self.callback()

				else:
					messagebox.showinfo(data["title"], "Row failed to be added")
