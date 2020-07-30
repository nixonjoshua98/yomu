

import tkinter as tk

from .childwindow import ChildWindow
from .widgets import Treeview


class SearchView(ChildWindow):
	def __init__(self, *, results, database):
		super(SearchView, self).__init__()

		# Window Configuration
		self.resizable(0, 0)

		self.results = results
		self.database = database

		self.tree: Treeview = None
		self.frame: tk.Frame = None

		self.center_in_root(400, 250)

		self.create()

		self.show()

	def create(self):
		self.frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		self.tree = Treeview(self.frame, headings=("Title",))

		self.tree.populate(map(lambda r: [r.title], self.results), use_iid=False)

		self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)