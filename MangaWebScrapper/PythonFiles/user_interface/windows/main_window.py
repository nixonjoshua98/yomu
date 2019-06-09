import threading

import tkinter as tk
import tkinter.ttk as ttk

import functions
import constants

import database.queries

import user_interface.widgets as widgets
import user_interface.windows as windows

import web_scrapper.enum2module


class Application(widgets.RootWindow):
	""" Class which will run the entire UI """

	table_headings = [
		"ID", "Manga Title", "Chapter Read", "Latest Chapter"
	]

	def __init__(self, download_controller):
		# ------------------------------------------ #
		super().__init__("Web Scrapper", "800x400")

		self.download_controller = download_controller
		self.sort_function = functions.sort_manga_by_chapters_available

		# - Create attributes
		self.table = None
		self.status_dropdown = None
		self.search_entry = None
		self.search_btn = None
		self.right_click = None

		self.current_searches = {**web_scrapper.enum2module.SEARCH_MODULES}

		self.child_windows = {
			"edit_window": None,
			"downloads_window": None,
			"search_results_window": None
		}

		# - Create the UI
		self.create_toolbar()
		self.create_table()
		self.create_right_click_menu()

		# - Post the right click menu on right click at cursor x, y
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
		table_callbacks = {"Double-1": self.on_row_selected}

		# - Frames
		table_frame = tk.Frame(self)

		# - Widgets
		self.table = widgets.Treeview(table_frame, self.table_headings, (50, 500, 100, 100), table_callbacks)

		# - Widget placement
		table_frame.pack(expand=True, fill=tk.BOTH)
		self.table.pack(expand=True, fill=tk.BOTH)

		self.update_table()

	def create_right_click_menu(self):
		self.right_click = tk.Menu(self.table, tearoff=0)

		sort_menu = tk.Menu(self.right_click, tearoff=0)
		open_in_menu = tk.Menu(self.right_click, tearoff=0)

		sort_menu.add_command(label="ID (asc)", command=self.sort_manga_by_id)
		sort_menu.add_command(label="Title (asc)", command=self.sort_manga_by_title)
		sort_menu.add_command(label="Latest Chapter (dsc)", command=self.sort_manga_by_latest_chapter)
		sort_menu.add_command(label="Chapters Available (dsc)", command=self.sort_manga_by_chapters_available)

		open_in_menu.add_command(label="Explorer", command=self.open_manga_in_explorer)
		open_in_menu.add_command(label="Browser", command=self.open_manga_in_browser)

		self.right_click.add_cascade(label="Open In", menu=open_in_menu)
		self.right_click.add_cascade(label="Sort Table", menu=sort_menu)

	""" Re-populate the table with the database results """
	def update_table(self):
		query_results = database.queries.manga_select_all_with_status(self.status_dropdown.get_index())

		if query_results is None:
			return

		# Do sorting
		if self.sort_function is not None:
			self.sort_function(query_results)

		# Too long a function name
		remove_zero = functions.remove_trailing_zeros_if_zero

		data = []
		for row in query_results:
			data.append((row.id, row.title, remove_zero(row.chapters_read), remove_zero(row.latest_chapter), row.url))

		self.table.clear()
		self.table.populate(data)

	""" Row double click callback - Allow the user to view and edit the row """
	def on_row_selected(self, event=None):
		row = self.table.one()

		if row is None:
			return

		db_row = database.queries.manga_select_one_with_id(row[0])

		try:
			self.child_windows["edit_window"].destroy()
		except AttributeError:
			""" Window is None (this is expected) """

		self.child_windows["edit_window"] = windows.MangaEditWindow(db_row, self.update_table)
		self.child_windows["edit_window"].center_in_root(500, 300)

	""" Toggles the queue window between being visible and hidden """
	def toggle_downloads_window(self, event=None):
		""" Create the downloads window if it hasn't been created before,
		I only want one downloads window to be created """
		if self.child_windows["downloads_window"] is None:
			win = windows.DownloadsWindow(self.download_controller)
			self.child_windows["downloads_window"] = win

		self.child_windows["downloads_window"].show_window()
		self.child_windows["downloads_window"].center_in_root(500, 300)

	def search_btn_callback(self, event=None):
		search_input = self.search_entry.get()

		# Min 3 characters
		if len(search_input) < 3:
			return

		self.search_btn.state(["disabled"])

		# Create a new thread so it doesn't block the main thread
		for k, module in self.current_searches.items():
			new_search = web_scrapper.enum2module.MODULE_TABLE[k].Search(search_input)

			self.current_searches[k] = new_search

			threading.Thread(target=self.current_searches[k].start).start()

			functions.callback_once_true(self, "finished", new_search, lambda: self.search_finished_callback())

	def search_finished_callback(self):
		# Not all searches have finished
		if not all(map(lambda s: s.finished, list(self.current_searches.values()))):
			return

		self.search_btn.state(["!disabled"])

		search_results = {k: v.results for k, v in self.current_searches.items()}

		win = windows.SearchResultsWindow(search_results, ("Title", "Description"), self.update_table)
		win.geometry(self.geometry())

		if self.child_windows["search_results_window"] is not None:
			self.child_windows["search_results_window"].destroy()

		self.child_windows["search_results_window"] = win

	""" Right click callbacks """

	def sort_manga_by_title(self):
		self.sort_function = functions.sort_manga_by_title
		self.update_table()

	def sort_manga_by_id(self):
		self.sort_function = functions.sort_manga_by_id
		self.update_table()

	def sort_manga_by_latest_chapter(self):
		self.sort_function = functions.sort_manga_by_latest_chapter
		self.update_table()

	def sort_manga_by_chapters_available(self):
		self.sort_function = functions.sort_manga_by_chapters_available
		self.update_table()

	def open_manga_in_explorer(self):
		row = self.table.one()

		if row is not None:
			functions.open_manga_in_explorer(row[1])

	def open_manga_in_browser(self):
		row = self.table.one()

		if row is not None:
			functions.open_manga_in_browser(row[4])
