import tkinter as tk
from tkinter import ttk


class Table(ttk.Treeview):
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

        super(Table, self).pack(**kwargs)
