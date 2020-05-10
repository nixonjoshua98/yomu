import tkinter as tk

from mangatracker.common.database import Database

from mangatracker.interface.toolbar import Toolbar
from mangatracker.interface.tableview import TableView


def migrate():
    db = Database()

    new_db = Database("D:\\Program Files\\OneDrive\\manga.sqlite3")

    for row in db.fetch("SELECT * FROM manga;"):
        params = (row["title"], row["url"], row["chapters_read"], row["latest_chapter"], row["status"])

        new_db.execute(
            "INSERT INTO manga (title, url, chapters_read, latest_chapter, status) VALUES (?, ?, ?, ?, ?);",
            *params
        )


class Application(tk.Tk):
    def __init__(self):
        super(Application, self).__init__()

        self.title("Manga Tracker")
        self.geometry("800x400")

        self._db = Database()

        root_frame = tk.Frame()

        # Create widgets
        self.toolbar = Toolbar(root_frame)
        self.table = TableView(root_frame)

        # Configure widgets
        self.toolbar.combo.set_command(self.on_combo_change)

        # Place widgets
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)
        self.table.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        root_frame.pack(expand=True, fill=tk.BOTH)

    def on_combo_change(self, event):
        pass

