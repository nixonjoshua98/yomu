import re

import tkinter as tk

from tkinter import messagebox

from .childwindow import ChildWindow
from .widgets import Treeview


class SearchView(ChildWindow):
	def __init__(self, *, results, database):
		super(SearchView, self).__init__()

		# Window Configuration
		self.resizable(0, 0)

		# Add an ID
		self.results = results

		self.database = database

		self.tree: Treeview = None
		self.frame: tk.Frame = None

		self.center_in_root(400, 250)

		self.create()

		self.show()

	def insert_entry(self, event):
		if not (iid := event.widget.focus()):
			return None

		cached_row = self.results[int(iid)]

		row = dict(title=cached_row.title, url=cached_row.url, latest_chapter=0, chapters_read=0, status=0)

		entries = list(self.database["manga"].find({"title": re.compile(row["title"], re.IGNORECASE)}))

		if entries:
			entries = "\n".join(map(lambda e: f"• {e['title']}", entries))
			s = f"{entries}\n\nDo you still want to add the manga?"

			if not messagebox.askyesno("Found similar existing title(s)", s):
				return None

		self.database["manga"].insert_one(row)

	def create(self):
		self.frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		self.tree = Treeview(self.frame, headings=("Title",))

		self.tree.bind("<Double-1>", self.insert_entry)

		self.tree.populate([[i, r.title] for i, r in enumerate(self.results)])

		self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
