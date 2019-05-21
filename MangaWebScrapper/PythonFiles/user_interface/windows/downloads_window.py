import tkinter as tk
import tkinter.ttk as ttk

import user_interface.widgets as widgets


class DownloadsWindow(widgets.ChildWindow):
	tree_headings = ["Manga Title", "Chapter No"]

	def __init__(self):
		super().__init__("Downloads", destroy_on_exit=False)

		# - Frames
		tree_frame = ttk.Frame(self)

		# - Table
		self.table = widgets.Treeview(
			tree_frame, 
			DownloadsWindow.tree_headings)

		# - Placements
		tree_frame.pack(expand=True, fill=tk.BOTH)

		self.table.pack(expand=True, fill=tk.BOTH)

		self.update_table()

	def update_table(self):
		val = (("Poop", "Poop"),)

		if val is not None:
			self.table.populate(val)

		self.after(1000, self.update_table)

