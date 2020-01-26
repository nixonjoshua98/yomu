import tkinter as tk
import tkinter.ttk as ttk

import user_interface.widgets as widgets


class DownloadsWindow(widgets.ChildWindow):
	tree_headings = ["Title", "Chapter No"]

	def __init__(self, download_controller):
		super().__init__("Downloads", destroy_on_exit=False)

		self.download_controller = download_controller

		# - Frames
		tree_frame = ttk.Frame(self)

		# - Table
		self.table = widgets.Treeview(tree_frame, self.tree_headings)

		# - Placements
		tree_frame.pack(expand=True, fill=tk.BOTH)

		self.table.pack(expand=True, fill=tk.BOTH)

		self.update_table()

	def update_table(self):
		val = self.download_controller.queue.pop()

		if val is not None:
			self.table.populate([val], top_down=True)

		self.after(500, self.update_table)

