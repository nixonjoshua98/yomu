import _functions

import tkinter as tk
import user_interface.widgets as widgets
import database.database_queries as database_queries
from tkinter import messagebox


class SearchResultsWindow(widgets.ChildWindow):
	def __init__(self, search_results, headers: tuple, callback):
		super().__init__(f"Search Results ({len(search_results)} results)", destroy_on_exit=True)

		self.callback = callback
		self.search_results = search_results

		table_callbacks = {"Button-3": self.add_manga_to_database}

		# - Frames
		table_frame = tk.Frame(self)

		# - Widgets
		table = widgets.Treeview(table_frame, headers, binds=table_callbacks)

		# - Placements
		table_frame.pack(expand=True, fill=tk.BOTH)
		table.pack(expand=True, fill=tk.BOTH)

		table.populate(list(map(lambda r: (r.title, r.latest_chapter), search_results)))

	def add_manga_to_database(self, event=None):
		row = event.widget.one()

		if row is not None:
			row_index = _functions.find_obj_with_attr("title", row[0], self.search_results)

			title = self.search_results[row_index].title
			url = self.search_results[row_index].url

			# Check if already in database
			if database_queries.manga_select_one_with_title(title):
				messagebox.showinfo(title, "Row with the same title already exists in the database")

			else:
				data = {"title": title, "url": url}

				if messagebox.askyesno("Database", f"Are you sure you want to add '{title}'"):
					if database_queries.manga_insert_row(**data):
						messagebox.showinfo("Database", title + " has been added")

						self.destroy()
						self.callback()

					else:
						messagebox.showinfo(title, "Row failed to be added")
