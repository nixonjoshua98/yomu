import tkinter as tk
import tkinter.ttk as ttk

import user_interface.widgets as widgets
import resources.constants as constants
import user_interface.windows as windows
import database.database_queries as queries

from functions.functions import (
    remove_trailing_zeros_if_zero
)


class Application(widgets.RootWindow):
	""" Class which will run the entire UI """

	table_headings = [
		"ID", "Manga Title", "Latest Chapter Read"
	]

	def __init__(self):
		# ------------------------------------------ #
		super().__init__("Web Scrapper", "800x500")

		# - Create attributes
		self.table = None
		self.status_dropdown = None

		# - Create the UI
		self.create_toolbar()
		self.create_table()

		# - Create extra windows
		self.downloads_window = windows.DownloadsWindow()

		# - Initial calls
		self.downloads_window.hide_window()

	"""
	Creates the toolbar which is located at the top of the window,
	all toolbar UI widgets should be created in this method
	"""
	def create_toolbar(self):
		# - Frames
		toolbar_frame = tk.Frame(self, relief = tk.SUNKEN, borderwidth = 1)
		btn_frame = tk.Frame(toolbar_frame, relief = tk.RAISED, borderwidth = 1)
		dropdown_frame = tk.Frame(toolbar_frame, relief = tk.RAISED, borderwidth = 1)

		# - Left side widgets
		self.status_dropdown = widgets.Dropdown(dropdown_frame, constants.MANGA_STATUS, self.update_table)

		# - Right side widgets
		downloads_btn = ttk.Button(btn_frame, text = "Downloads", command = self.toggle_downloads_window)
		search_btn = ttk.Button(btn_frame, text = "Search")

		# - Widget placement
		toolbar_frame.pack(fill = tk.X)
		dropdown_frame.pack(side = tk.LEFT, fill = tk.X, padx = 3, pady = 3)
		btn_frame.pack(side = tk.RIGHT, fill = tk.X, padx = 3, pady = 3)

		self.status_dropdown.pack(side = tk.LEFT, padx = 3, pady = 3)

		search_btn.pack(side = tk.RIGHT, padx = 3, pady = 3)
		downloads_btn.pack(side = tk.RIGHT, padx = 3, pady = 3)

	"""
	Creates the main treeview table which is used to display
	the data queried from the database
	"""
	def create_table(self):
		# - Variables
		table_callbacks = {
			"Double-1": self.on_row_selected
		}

		# - Frames
		table_frame = tk.Frame(self)

		# - Widgets
		self.table = widgets.Treeview(table_frame, self.table_headings, [50, 300], table_callbacks)

		# - Widget placement
		table_frame.pack(expand = True, fill = tk.BOTH)
		self.table.pack(expand = True, fill = tk.BOTH)

		self.update_table()

	"""
	Re-populate the table with the database results
	"""
	def update_table(self):
		q = queries.manga_select_with_status(self.status_dropdown.get_index())

		if q is None:
			return

		data = [[row.id, row.title, remove_trailing_zeros_if_zero(row.chapters_read)] for row in q]

		self.table.clear()
		self.table.populate(data)

	"""
	Row double click callback - Allow the user to view and edit the row
	"""
	def on_row_selected(self, event=None):
		row = self.table.one()

		if row is None:
			return

		db_row = queries.manga_select_with_id(row[0])

		windows.MangaEditWindow(db_row, self.update_table)

	"""
	Toggles the queue window between being visible and hidden
	"""
	def toggle_downloads_window(self, event=None):
		if self.downloads_window.is_hidden:
			self.downloads_window.geometry(self.geometry())
			self.downloads_window.show_window()
		else:
			self.downloads_window.hide_window()
