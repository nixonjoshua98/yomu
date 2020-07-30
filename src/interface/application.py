import webbrowser

from typing import List, Dict

from manganelo import SearchManga

import tkinter as tk
import tkinter.ttk as ttk

import functools as ft

from src import utils
from src.statuses import Statuses

from .mangaview import MangaView
from .searchview import SearchView
from .widgets import Treeview, ComboBox


class Application(tk.Tk):
	def __init__(self, *, database, worker):
		super(Application, self).__init__()

		self.database = database
		self.worker = worker

		# Window configuration
		self.wm_title("Manga")
		self.geometry("800x400")
		self.resizable(0, 0)

		self.tree: Treeview = None
		self.tree_data: List[Dict] = list()
		self.combo_val: str = None

		self.filters = dict(readable_only=tk.BooleanVar(value=True))

		self.create()

		self.update_tree(text=self.combo_val)

	def create(self):
		""" Create the interface widgets. """

		# - - - Tool Bar - - - #
		frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		combo = ComboBox(frame, values=Statuses.all_text, command=self.on_status_change)
		combo.pack(side=tk.LEFT, padx=5, pady=5)

		search_entry = ttk.Entry(frame)
		search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

		search_btn = ttk.Button(frame, text="Search")
		search_btn.config(command=ft.partial(self.on_search_btn,search_btn, search_entry))
		search_btn.pack(side=tk.LEFT, padx=5, pady=5)

		frame.pack(fill=tk.X, padx=5, pady=5)

		# - - - Filter Menu - - - #
		frame = tk.Frame(self)

		c = tk.Checkbutton(
			frame,
			text="Readable",
			variable=self.filters["readable_only"],
			command=self.on_filter_update
		)

		c.pack(side=tk.LEFT)

		frame.pack(fill=tk.X, padx=5)

		# - - - Treeview - - - #
		frame = tk.Frame(self)

		self.tree = Treeview(
			frame,
			headings=("Title", "Chapter Read", "Latest Chapter"),
			widths=(500, 125, 125)
		)

		self.tree.bind("<Double-1>", self.on_row_select)
		self.tree.bind("<FocusIn>", self.on_tree_focus)
		self.tree.pack(fill=tk.BOTH, expand=True)

		frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		# - - - Menu - - - #
		menu = tk.Menu(self.tree, tearoff=0)

		menu.add_command(label="Open in Browser", command=self.open_in_browser)

		self.tree.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

		# - - - Attributes - - - #
		self.combo_val = combo.get()

	def update_tree(self, **kwargs):
		def get_row(d):
			row = [d[k] for k in ("_id", "title", "chapters_read", "latest_chapter")]

			row[2] = int(row[2]) if str(row[2]).endswith(".0") else row[2]
			row[3] = int(row[3]) if str(row[3]).endswith(".0") else row[3]

			return row

		kwargs["text"] = kwargs.get("text", self.combo_val)

		status = Statuses.get(**kwargs)

		self.tree.clear()

		# SELECT WHERE status = status['id]
		match = {"$match": {"$and": [{"status": status["id"]}]}}

		# ADD FIELD _chapters = latest_chapter - chapters_read
		fields = {"$addFields": {"_chapters": {"$subtract": ["$latest_chapter", "$chapters_read"]}}}

		# SORT BY _chapters DESC
		sort = {"$sort": {"_chapters": -1}}

		# Query modification based on filters
		if self.filters["readable_only"].get():
			match["$match"]["$and"].append({"_chapters": {"$gt": 0}})

		self.tree_data = list(self.database.manga.aggregate([fields, match, sort]))

		self.tree.populate(map(get_row, self.tree_data.copy()))

	def open_in_browser(self):
		if not (iid := self.tree.focus()):
			return None

		cached_row = utils.get(self.tree_data, _id=iid)

		webbrowser.open(cached_row["url"], new=False)

	def on_row_select(self, event):
		if not (iid := event.widget.focus()):
			return None

		cached_row = utils.get(self.tree_data, _id=iid)

		_ = MangaView(values=cached_row, database=self.database)

	def on_search_btn(self, btn, entry: ttk.Entry):
		if len(query := entry.get()) < 3:
			return None

		def decorator():
			results = tuple(search.results())

			btn.state(["!disabled"])

			_ = SearchView(results=results, database=self.database)

		btn.state(["disabled"])

		search = SearchManga(query, threaded=True)

		self.after(2000, decorator)

	def on_status_change(self, event):
		self.combo_val = event.widget.get()

		self.update_tree()

	def on_filter_update(self):
		self.update_tree()

	def on_tree_focus(self, _):
		self.update_tree()
