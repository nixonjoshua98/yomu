import functions
import database.queries
import user_interface.widgets

import functools as ft
import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox


class SearchResultsWindow(user_interface.widgets.ChildWindow):
	def __init__(self, search_results, headers: tuple, callback):
		super().__init__("Search Results", destroy_on_exit=True)

		self.callback = callback
		self.search_results = search_results

		table_callbacks = {"Button-3": self.add_manga_to_database}

		frame = tk.Frame(self)

		table = user_interface.widgets.Treeview(frame, headers, binds=table_callbacks)

		table.pack(expand=True, fill=tk.BOTH)

		table.populate(list(map(lambda r: (r.title, r.desc), search_results)))

		frame.pack(expand=True, fill=tk.BOTH)

	def add_manga_to_database(self, event=None):
		row = event.widget.one()

		if row is None:
			return

		row_index = functions.find_obj_with_attr("title", row[0], self.search_results)

		url = self.search_results[row_index].url
		title = self.search_results[row_index].title

		# Check if already in database
		if database.queries.manga_select_one_with_title(title):
			messagebox.showinfo(title, "Row with the same title already exists in the database")
			return

		data = {"title": title, "url": url}

		if messagebox.askyesno("Database", f"Are you sure you want to add '{title}'"):
			if database.queries.manga_insert_row(**data):
				messagebox.showinfo("Database", title + " has been added")

				self.destroy()
				self.callback()

			else:
				messagebox.showinfo(title, "Row failed to be added")
