import tkinter as tk

from tkinter import ttk


class ChildWindow(tk.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(ChildWindow, self).__init__(master=master, *args, **kwargs)

	def show(self):
		self.grab_set()
		self.wait_window()

	def center_in_root(self, w, h):
		master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
		master_w, master_h = self.master.winfo_width(), self.master.winfo_height()

		win_w, win_h = w, h

		center_x = master_x + (master_w // 2) - (win_w // 2)
		center_y = master_y + (master_h // 2) - (win_h // 2)

		self.geometry(f"{win_w}x{win_h}+{center_x}+{center_y}")


class ComboBox(ttk.Combobox):
	def __init__(self, master, values, command=None):
		super().__init__(master, state="readonly", values=values)

		self.current(0)

		self.bind("<<ComboboxSelected>>", command)


class Treeview(ttk.Treeview):
	def __init__(self, master, headings: list, *, widths: list = None):
		super().__init__(master=master, columns=headings, show="headings")

		self.scroll = ttk.Scrollbar(master)

		self.configure(yscrollcommand=self.scroll.set)
		self.scroll.configure(command=self.yview)

		for i, col in enumerate(self["columns"]):
			self.heading(col, text=col)

			self.column(col, minwidth=125, width=0, stretch=tk.YES)

			if widths is not None and i < len(widths):
				self.column(col, minwidth=widths[i], width=widths[i], stretch=tk.YES)

	def populate(self, data):

		self.clear()

		for i, row in enumerate(data):
			self.insert("", 0, iid=row[0], values=row[1:])

	def clear(self):
		self.delete(*self.get_children())

	def pack(self, **kwargs):
		self.scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=kwargs.get("pady", 0))

		super(Treeview, self).pack(**kwargs)


