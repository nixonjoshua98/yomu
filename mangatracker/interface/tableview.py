import tkinter as tk

from mangatracker.common.queries import MangaSQL
from mangatracker.common.database import Database

from mangatracker.interface.treeview import Treeview


class TableView(tk.Frame):
    def __init__(self, master=None):
        super(TableView, self).__init__(master=master)

        headings, widths = ("ID", "Title", "Chapters Read", "Latest Chapter"), (40, 500, 110, 110)

        self._db = Database()

        self.tree = Treeview(self, headings, widths)

        self.update_tree(status=0)

        self.tree.pack(expand=True, fill=tk.BOTH)

    def update_tree(self, *, status: int):
        def subset_dict(d: dict, default=None):
            return [d.get(k, default) for k in keys]

        rows = self._db.fetch(MangaSQL.SELECT_STATUS, status)
        keys = ("mangaID", "title", "chapters_read", "latest_chapter")

        self.tree.populate(map(subset_dict, rows))
