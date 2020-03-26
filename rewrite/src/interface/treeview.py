import tkinter as tk

from tkinter import ttk


class Treeview(ttk.Treeview):
	def __init__(self, master, headings: list):
		super(Treeview, self).__init__(master=master, columns=headings, show="headings")

		self.scroll = ttk.Scrollbar(master)

		self.configure(yscrollcommand=self.scroll.set)
		self.scroll.configure(command=self.yview)

		self.reset()

		self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

	def populate(self, data, top_down=False):
		for i, d in enumerate(data):
			self.insert("", 0 if top_down else "end", values=d)

	def clear(self):
		self.delete(*self.get_children())

	def reset(self):
		for i, col in enumerate(self["columns"]):
			if i in (0, ):
				self.column(col, minwidth=50, width=50, stretch=False)

			elif i in (2, 3):
				self.column(col, minwidth=150, width=150, stretch=False)

			self.heading(col, text=col)

	def one(self):
		try:
			item = self.item(self.selection()[0])["values"]
		except IndexError:
			return None
		else:
			return item
