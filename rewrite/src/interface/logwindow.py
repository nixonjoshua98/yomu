import tkinter as tk

from . import (Toplevel, Treeview)


class LogWindow(Toplevel):
    def __init__(self):
        super(LogWindow, self).__init__("Manga Tracker - Log", geometry="400x300", destroy_on_exit=False)

        self.tree = Treeview(self, ["Log"])

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.withdraw()

    def show(self):
        self.deiconify()

        self.center_in_root()

    def add(self, row):
        self.tree.populate([row])
