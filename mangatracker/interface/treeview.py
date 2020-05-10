import typing

import tkinter as tk

from tkinter import ttk


class Treeview(ttk.Treeview):
    def __init__(self, master, headings: typing.Sequence, col_widths: typing.Sequence = None):
        super().__init__(master=master, columns=headings, show="headings")

        self.col_widths = [] if col_widths is None else col_widths

        self.scroll = ttk.Scrollbar(master)

        self.configure(yscrollcommand=self.scroll.set)
        self.scroll.configure(command=self.yview)

        self.reset()

        self.scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

    def populate(self, data, from_top=False):
        for i, d in enumerate(data):
            self.insert("", 0 if from_top else "end", values=d)

    def clear(self):
        self.delete(*self.get_children())

    def reset(self):
        for i, col in enumerate(self["columns"]):
            self.heading(col, text=col)

            if i < len(self.col_widths) and self.col_widths[i] is not None:
                self.column(col, minwidth=self.col_widths[i] // 2, width=self.col_widths[i], stretch=True)
