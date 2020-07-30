import tkinter as tk

from tkinter import ttk


class ComboBox(ttk.Combobox):
	def __init__(self, master, values, command=None):
		super().__init__(master, state="readonly", values=values)

		self.current(0)

		self.bind("<<ComboboxSelected>>", command)


class Treeview(ttk.Treeview):
	def __init__(self, master, headings: list, *, widths: list = None):
		super().__init__(master=master, columns=headings, show="headings")

		self.widths = widths

		self.scroll = ttk.Scrollbar(master)

		self.configure(yscrollcommand=self.scroll.set)
		self.scroll.configure(command=self.yview)

		for i, col in enumerate(self["columns"]):
			self.heading(col, text=col)

			self.column(col, minwidth=125, width=0, stretch=tk.YES)

			if self.widths is not None and i < len(self.widths):
				self.column(col, minwidth=self.widths[i], width=self.widths[i], stretch=tk.YES)

	def populate(self, data, *, top_down=False, use_iid=True):
		for i, row in enumerate(data):
			if use_iid:
				self.insert("", 0 if top_down else "end", iid=row[0], values=row[1:])
			else:
				self.insert("", 0 if top_down else "end", values=row)

	def clear(self):
		self.delete(*self.get_children())

	def pack(self, **kwargs):
		self.scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=kwargs.get("pady", 0))

		super(Treeview, self).pack(**kwargs)


