import tkinter as tk

from tkinter import ttk


class Treeview(ttk.Treeview):
	def __init__(self, master, headings: list, widths: list = None):
		super(Treeview, self).__init__(master=master, columns=headings, show="headings")

		self.scroll = ttk.Scrollbar(master)

		self.configure(yscrollcommand=self.scroll.set)
		self.scroll.configure(command=self.yview)

		self.widths = widths if widths is not None else []

		self.reset()

		self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

	def populate(self, data, top_down=False):
		for i, d in enumerate(data):
			self.insert("", 0 if top_down else "end", values=d)

	def clear(self):
		self.delete(*self.get_children())

	def reset(self):
		for i, col in enumerate(self["columns"]):
			self.heading(col, text=col)

			try:
				w = self.widths[i]

				if w is None:
					continue

				self.column(col, minwidth=w, width=w, stretch=False)

			except IndexError as e:
				pass

	def one(self):
		try:
			item = self.item(self.selection()[0])["values"]
		except IndexError:
			return None
		else:
			return item
