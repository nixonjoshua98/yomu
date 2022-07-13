import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from src import utils
from src.models import Story
from src.childwindow import ChildWindow
from src.datasources import MangakatanaDataSource, ManganeloDataSource, DataSourceSearchResult
from src.table import Table


class StorySearchWindow(ChildWindow):
    def __init__(self, query, data_storage):
        super(StorySearchWindow, self).__init__()

        self.results = []
        self.data_storage = data_storage
        self.notebook = self.create_notebook()

        self._configure_window()

        self.pull_results(
            query, ManganeloDataSource, self.create_results_tree("Manganelo")
        )
        self.pull_results(
            query, MangakatanaDataSource, self.create_results_tree("MangaKatana")
        )

        self.show()

    def _configure_window(self):
        self.resizable(0, 0)
        self.center_in_root(400, 250)

    @staticmethod
    def pull_results(query, datasource, tree):
        utils.run_in_pool(lambda: datasource.search(query), lambda results: tree.populate(results))

    def create_notebook(self):
        notebook = ttk.Notebook(self)

        notebook.pack(fill=tk.BOTH, expand=True)

        return notebook

    def create_results_tree(self, title):
        frame = tk.Frame(self.notebook, relief=tk.RAISED, borderwidth=1)

        tree = TreeViewResults(frame, self.data_storage, headings=["Result"])

        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.notebook.add(frame, text=title)

        return tree


class TreeViewResults(Table):
    def __init__(self, master, data_storage, **kwargs):
        super(TreeViewResults, self).__init__(master, **kwargs)

        self.results: list[DataSourceSearchResult] = []
        self._data_storage = data_storage

        self.bind("<Double-1>", self.on_click)

    def populate(self, data):
        self.results = data

        super().populate(([i, r.title] for i, r in enumerate(data)))

    def on_click(self, event):

        # Invalid iid (ignore the event)
        if not (iid := event.widget.focus()):
            return None

        row = self.results[int(iid)]

        story = Story(
            title=row.title,
            url=row.url,
            status=0
        )

        self._data_storage.insert_story(story)

        messagebox.showinfo("Success", f"Added '{row.title}'")
