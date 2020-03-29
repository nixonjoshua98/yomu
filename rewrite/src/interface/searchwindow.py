import tkinter as tk

from . import (Toplevel, Treeview)


class SearchWindow(Toplevel):
    _prev_instance = None

    def __init__(self, search_results: list):
        super(SearchWindow, self).__init__("Manga Tracker - Search Results", geometry="600x300", destroy_on_exit=False)

        # Allow only one instance of this window
        if SearchWindow._prev_instance is not None:
            SearchWindow._prev_instance.withdraw()

        SearchWindow._prev_instance = self

        self.tree = Treeview(self, ["Title"])

        self.tree.populate(map(lambda ele: [ele.title], search_results))

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.center_in_root()

    @classmethod
    def show_previous(cls):
        if cls._prev_instance is not None:
            cls._prev_instance.center_in_root()
            cls._prev_instance.deiconify()

