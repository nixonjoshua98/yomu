
import webbrowser

from typing import Optional

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

import functools as ft

from src import storage
from src.statuses import StatusList

from src.combobox import ComboBox

from src.widgets import Treeview
from src.editwindow import StoryEditWindow
from src.searchwindow import StorySearchWindow
from src.jsonstorage import JSONStorage


class Application(tk.Tk):
	def __init__(self):
		super(Application, self).__init__()

		self._data = JSONStorage()

		self._configure_window()

		self.tree = None
		self.tree_data = list()

		# - - - Widgets - - - #
		self.status_combo: Optional[ComboBox] = None

		self.filters = {"readable_only": tk.BooleanVar(value=True)}

		self.create()

		self.update_tree()

	@property
	def current_status(self): return self.status_combo.current_value

	def _configure_window(self):
		self.wm_title("Manga")
		self.geometry("800x400")
		self.resizable(0, 0)

	def create(self):
		""" Create the windows widgets. """

		# - - - Tool Bar - - - #
		frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		self.status_combo = ComboBox(frame, command=lambda e: self.update_tree())
		self.status_combo.add_options([[status.display_text, status.id] for status in StatusList])
		self.status_combo.pack(side=tk.LEFT, padx=5, pady=5)

		search_entry = ttk.Entry(frame)
		search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

		search_btn = ttk.Button(frame, text="Search")
		search_btn.config(command=ft.partial(self.on_search_btn, search_entry))
		search_btn.pack(side=tk.LEFT, padx=5, pady=5)

		frame.pack(fill=tk.X, padx=5, pady=5)

		# - - - Filter Menu - - - #
		frame = tk.Frame(self)

		c = tk.Checkbutton(
			frame,
			text="Readable",
			variable=self.filters["readable_only"],
			command=self.update_tree
		)

		c.pack(side=tk.LEFT)

		frame.pack(fill=tk.X, padx=5)

		# - - - Treeview - - - #
		frame = tk.Frame(self)

		self.tree = Treeview(
			frame,
			headings=["Title", "Chapter Read", "Latest Chapter"],
			widths=[500, 125, 125]
		)

		self.tree.bind("<Double-1>", self.on_row_select)

		self.tree.pack(fill=tk.BOTH, expand=True)

		frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		# - - - Menu - - - #
		menu = tk.Menu(self.tree, tearoff=0)

		menu.add_command(label="Open in Browser", command=self.open_in_browser)

		self.tree.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

	def update_tree(self):

		def to_list(d):
			return [d[k] for k in ("_id", "title", "chapters_read", "latest_chapter")]

		self.tree_data = storage.get().get_all_with_status(
			self.current_status, readable_only=self.filters["readable_only"].get()
		)

		self.tree_data.reverse()

		self.tree.populate(map(to_list, self.tree_data))

	def open_in_browser(self):
		if iid := self.tree.focus():
			row = storage.get().find_one(iid)

			webbrowser.open(row["url"], new=False)

	@staticmethod
	def on_row_select(event):
		if iid := event.widget.focus():
			StoryEditWindow(iid)

	@staticmethod
	def on_search_btn(entry: ttk.Entry):

		if len(query := entry.get()) < 3:
			return messagebox.showerror("Search Query", "Search query is too short.")

		StorySearchWindow(query)
