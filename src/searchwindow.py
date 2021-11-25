import functools as ft
import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox

from src import utils

from src.datasources import ManganeloDataSource, MangaKatanaDataSource

from src.table import Table
from src.childwindow import ChildWindow


class StorySearchWindow(ChildWindow):
	def __init__(self, query, data_storage):
		super(StorySearchWindow, self).__init__()

		self.results = []
		self.data_storage = data_storage
		self.notebook = self.create_notebook()

		self._configure_window()

		self.pull_results(query, ManganeloDataSource, self.create_results_tree("Manganelo"))
		self.pull_results(query, MangaKatanaDataSource, self.create_results_tree("MangaKatana"))

		self.show()

	def _configure_window(self):
		self.resizable(0, 0)
		self.center_in_root(400, 250)

	@staticmethod
	def pull_results(query, datasource, tree):

		def callback(results):
			tree.populate(results)

		utils.run_in_pool(ft.partial(datasource.search, query), callback)

	def create_notebook(self):
		notebook = ttk.Notebook(self)

		notebook.pack(fill=tk.BOTH, expand=True)

		return notebook

	def create_results_tree(self, title):
		frame = tk.Frame(self.notebook, relief=tk.RAISED, borderwidth=1)

		tree = TreeViewResults(frame, self.data_storage, headings=["Result"])

		tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
		frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		self.notebook.add(frame, text=title)

		return tree


class TreeViewResults(Table):
	def __init__(self, master, data_storage, **kwargs):
		super(TreeViewResults, self).__init__(master, **kwargs)

		self.results = []
		self._data_storage = data_storage

		self.bind("<Double-1>", self.on_click)

	def populate(self, data):
		self.results = data

		super().populate(([i, r.title] for i, r in enumerate(data)))

	def on_click(self, event):

		# Invalid iid (ignore the event)
		if not (iid := event.widget.focus()):
			return None

		row = self.results[int(iid)]

		self._data_storage.insert_one(row.title, row.url, 0)

		messagebox.showinfo("Sucess", f"Added {row.title}")
