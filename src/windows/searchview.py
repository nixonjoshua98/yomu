
import tkinter as tk
import tkinter.messagebox as messagebox

from src import storage

from src.widgets import Treeview, ChildWindow


class SearchView(ChildWindow):
	def __init__(self, results):
		super(SearchView, self).__init__()

		self.results = results

		self._configure_window()

	def _configure_window(self):
		self.resizable(0, 0)
		self.center_in_root(400, 250)

		self.create()
		self.show()

	def insert_entry(self, event):

		# Invalid iid (ignore the event)
		if not (iid := event.widget.focus()):
			return None

		row = self.results[int(iid)]

		storage.get().insert_one(
			{"title": row.title, "url": row.url, "latest_chapter": 0, "chapters_read": 0, "status": 0}
		)

	def create(self):
		frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		tree = Treeview(frame, headings=["Title"])

		tree.bind("<Double-1>", self.insert_entry)

		tree.populate([[i, r.title] for i, r in enumerate(self.results)])

		tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
		frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
