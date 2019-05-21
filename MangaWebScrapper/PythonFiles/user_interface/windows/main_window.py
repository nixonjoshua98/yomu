import threading

import tkinter as tk
import tkinter.ttk as ttk

import user_interface.widgets as widgets
import user_interface.windows as windows

import resources.constants as constants
import database.database_queries as database_queries
import scrapper.scrapper_manganelo as scrapper_manganelo
import functions.functions as functions


class Application(widgets.RootWindow):
	""" Class which will run the entire UI """

	table_headings = [
		"ID", "Manga Title", "Latest Chapter Read"
	]

	def __init__(self, download_controller):
		# ------------------------------------------ #
		super().__init__("Web Scrapper", "800x500")

		self.download_controller = download_controller

		# - Create attributes
		self.table = None
		self.status_dropdown = None
		self.search_entry = None
		self.search_btn = None
		self.right_click = None
		self.sort_function = None
		self.current_search = None

		self.child_windows = {
			"edit_window": None,
			"downloads_window": None,
			"search_results_window": None
		}

		# - Create the UI
		self.create_toolbar()
		self.create_table()
		self.create_right_click_menu()

		self.table.bind("<Button-3>", lambda e: self.right_click.post(e.x_root, e.y_root))

	"""
	Creates the toolbar which is located at the top of the window,
	all toolbar UI widgets should be created in this method
	"""
	def create_toolbar(self):
		# - Frames
		toolbar_frame = tk.Frame(self, relief=tk.SUNKEN, borderwidth=1)
		btn_frame = tk.Frame(toolbar_frame, relief=tk.RAISED, borderwidth=1)
		dropdown_frame = tk.Frame(toolbar_frame, relief=tk.RAISED, borderwidth=1)

		# - Left side widgets
		self.status_dropdown = widgets.Dropdown(dropdown_frame, constants.MANGA_STATUS, self.update_table)

		# - Right side widgets
		downloads_btn = ttk.Button(btn_frame, text="Downloads", command=self.toggle_downloads_window)
		self.search_entry = ttk.Entry(btn_frame)
		self.search_btn = ttk.Button(btn_frame, text="Search", command=self.search_btn_callback)

		# - Widget placement
		toolbar_frame.pack(fill=tk.X)
		dropdown_frame.pack(side=tk.LEFT, fill=tk.X, padx=3, pady=3)
		btn_frame.pack(side=tk.RIGHT, fill=tk.X, padx=3, pady=3)

		self.status_dropdown.pack(side=tk.LEFT, padx=3, pady=3)
		self.search_btn.pack(side=tk.RIGHT, padx=3, pady=3)
		self.search_entry.pack(side=tk.RIGHT, padx=3, pady=3)
		downloads_btn.pack(side=tk.RIGHT, padx=3, pady=3)

	""" Creates the main table which is used to display the data queried from the database """
	def create_table(self):
		# - Variables
		table_callbacks = {
			"Double-1": self.on_row_selected
		}

		# - Frames
		table_frame = tk.Frame(self)

		# - Widgets
		self.table = widgets.Treeview(table_frame, self.table_headings, (50, 500), table_callbacks)

		# - Widget placement
		table_frame.pack(expand=True, fill=tk.BOTH)
		self.table.pack(expand=True, fill=tk.BOTH)

		self.update_table()

	def create_right_click_menu(self):
		self.right_click = tk.Menu(self.table, tearoff=0)

		sort_menu = tk.Menu(self.right_click, tearoff=0)

		sort_menu.add_command(label="ID", command=self.sort_manga_by_id)
		sort_menu.add_command(label="Title", command=self.sort_manga_by_title)

		self.right_click.add_cascade(label="Sort Table", menu=sort_menu)

	""" Re-populate the table with the database results """
	def update_table(self):
		q = database_queries.manga_select_all_with_status(self.status_dropdown.get_index())

		if q is None:
			return

		if self.sort_function is not None:
			q = self.sort_function(q)

		data = [[row.id, row.title, functions.remove_trailing_zeros_if_zero(row.chapters_read)] for row in q]

		self.table.clear()
		self.table.populate(data)

	""" Row double click callback - Allow the user to view and edit the row """
	def on_row_selected(self, event=None):
		row = self.table.one()

		if row is None:
			return

		db_row = database_queries.manga_select_one_with_id(row[0])

		# Destroy the previous window (only have one open at one time)
		if self.child_windows["edit_window"] is not None:
			self.child_windows["edit_window"].destroy()
			self.child_windows["edit_window"] = None

		# Create the new window
		win = windows.MangaEditWindow(db_row, self.update_table)
		win.geometry(self.geometry())  # Update the position

		self.child_windows["edit_window"] = win

	""" Toggles the queue window between being visible and hidden """
	def toggle_downloads_window(self, event=None):
		""" Create the downloads window if it hasn't been created before,
		I only want one downloads window to be created """
		if self.child_windows["downloads_window"] is None:
			win = windows.DownloadsWindow(self.download_controller)
			win.geometry(self.geometry())

			self.child_windows["downloads_window"] = win

		else:  # Toggle the view between hidden and shown
			self.child_windows["downloads_window"].toggle_view()

	def search_btn_callback(self, event=None):
		search_input = self.search_entry.get()

		# Min 3 characters
		if len(search_input) < 3:
			return

		self.search_btn.state(["disabled"])

		self.current_search = scrapper_manganelo.Search(search_input)

		# Create a new thread so it doesn't block the main thread
		threading.Thread(target=self.current_search.start).start()

		# Keep checking if the search is finished
		functions.callback_once_true(self, self.current_search, lambda: self.search_finished_callback())

	def search_finished_callback(self):
		self.search_btn.state(["!disabled"])

		search_results = self.current_search

		self.current_search = None

		win = windows.SearchResultsWindow(search_results, ("Title", "Latest Chapter"), self.update_table)
		win.geometry(self.geometry())

		if self.child_windows["search_results_window"] is not None:
			self.child_windows["search_results_window"].destroy()

		self.child_windows["search_results_window"] = win

	def sort_manga_by_title(self):
		print(">>> Changing sort to 'Manga Title'")
		self.sort_function = functions.sort_manga_by_title
		self.update_table()

	def sort_manga_by_id(self):
		print(">>> Changing sort to 'Manga ID'")
		self.sort_function = functions.sort_manga_by_id
		self.update_table()


