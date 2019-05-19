import tkinter as tk

from tkinter import ttk


class Treeview(ttk.Treeview):
    def __init__(self, master, headings: list, col_widths: list = None, binds: dict = None):
        super().__init__(master=master, columns=headings, show="headings")

        self.col_widths = [] if col_widths is None else col_widths

        self.scroll = ttk.Scrollbar(self)

        self.configure(yscrollcommand=self.scroll.set)
        self.scroll.configure(command=self.yview)

        # Bind events to commands
        if isinstance(binds, dict):
            for k, v in binds.items():
                self.bind(f"<{k}>", v)

        self.reset()

        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Append rows to the treeview
    def populate(self, data, top_down=False):
        for i, d in enumerate(data):
            self.insert("", 0 if top_down else "end", values = d)

    # Clears the entire tree
    def clear(self):
        self.delete(*self.get_children())

    def reset(self):           
        for i, col in enumerate(self["columns"]):
            self.heading(col, text=col)

            if i < len(self.col_widths):
                self.column(col, minwidth=self.col_widths[i], width=self.col_widths[i], stretch=tk.NO)

    # Returns the first value which was selected
    def one(self):
        try:
            item = self.item(self.selection()[0])["values"]
        except IndexError:  # Normally this happens if the item selected is the column header
            return None
        else:
            return item
