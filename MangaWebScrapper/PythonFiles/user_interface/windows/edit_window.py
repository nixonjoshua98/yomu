import tkinter as tk
import tkinter.ttk as ttk

import _functions


import database.database_queries as database_queries
import user_interface.widgets as widgets

from database.database_models import Manga
from database.database_enums import MangaStatusEnum
from tkinter import messagebox


class MangaEditWindow(widgets.ChildWindow):
    def __init__(self, manga_data: Manga, success_callback):
        super().__init__(manga_data.title, resize=True, destroy_on_exit=True)

        self.manga_data = manga_data
        self.input_widgets = {}
        self.callback = success_callback

        # - Frames
        self.root_frame = ttk.Frame(self)

        self.create_field_inputs()

        # - Default Buttons
        confirm_btn = ttk.Button(self.root_frame, text="Confirm", command=self.confirm_callback)
        undo_btn = ttk.Button(self.root_frame, text="Undo", command=self.undo_callback)
        delete_btn = ttk.Button(self.root_frame, text="Delete", command=self.delete_callback)

        # - Placements
        self.root_frame.pack(fill=tk.X)
        confirm_btn.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)
        undo_btn.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)
        delete_btn.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

    def create_entry(self, parent, default_text, disabled=False) -> widgets.EntryField:
        entry = widgets.EntryField(parent)
        entry.set_text(default_text)

        if disabled:
            entry.state(["disabled"])

        entry.pack(side=tk.LEFT, fill=tk.X, padx=5, expand=True)

        return entry

    def create_dropdown(self, parent, values, initial_value_index) -> widgets.Dropdown:
        dropdown = widgets.Dropdown(parent, values, lambda: print())

        dropdown.current(initial_value_index)

        dropdown.pack(side=tk.RIGHT, fill=tk.X, padx=5, expand=True)

        return dropdown

    def create_field_inputs(self):
        # - ID (PK)
        row_frame = tk.Frame(self.root_frame)

        tk.Label(row_frame, text="Manga ID").pack(side=tk.LEFT, padx=5, fill=tk.X)

        self.input_widgets["id"] = self.create_entry(row_frame, self.manga_data.id, disabled=True)

        row_frame.pack(fill=tk.X, pady=5)

        # - Title
        row_frame = tk.Frame(self.root_frame)

        tk.Label(row_frame, text="Title").pack(side=tk.LEFT, padx=5, fill=tk.X)

        self.input_widgets["title"] = self.create_entry(row_frame, self.manga_data.title, disabled=True)

        row_frame.pack(fill=tk.X, pady=5)

        # - Menu URL
        row_frame = tk.Frame(self.root_frame)

        tk.Label(row_frame, text="Menu URL").pack(side=tk.LEFT, padx=5, fill=tk.X)

        self.input_widgets["url"] = self.create_entry(row_frame, self.manga_data.url)

        row_frame.pack(fill=tk.X, pady=5)

        # - Chapters Read
        row_frame = tk.Frame(self.root_frame)
        btn = ttk.Button(row_frame, text="Latest Chapter", command=self.latest_offline_callback)

        default_val = _functions.remove_trailing_zeros_if_zero(self.manga_data.chapters_read)

        tk.Label(row_frame, text="Chapters Read").pack(side=tk.LEFT, padx=5, fill=tk.X)

        self.input_widgets["chapters_read"] = self.create_entry(row_frame, default_val)

        btn.pack(side=tk.LEFT, padx=5)
        row_frame.pack(fill=tk.X, pady=5)

        # - Manga Status
        row_frame = tk.Frame(self.root_frame)
        tk.Label(row_frame, text="Status").pack(side=tk.LEFT, padx=5, fill=tk.X)

        initial_val_index = MangaStatusEnum(self.manga_data.status).value
        all_values = [e.prettify() for e in MangaStatusEnum]

        self.input_widgets["status"] = self.create_dropdown(row_frame, all_values, initial_val_index)

        row_frame.pack(fill=tk.X, pady=5)

    def undo_callback(self, event=None):
        chapters_read = _functions.remove_trailing_zeros_if_zero(self.manga_data.chapters_read)

        self.input_widgets["title"].set_text(self.manga_data.title)
        self.input_widgets["url"].set_text(self.manga_data.url)
        self.input_widgets["chapters_read"].set_text(chapters_read)
        self.input_widgets["status"].current(MangaStatusEnum(self.manga_data.status).value)

    def confirm_callback(self, event=None):
        chapters_read = self.input_widgets["chapters_read"].get()

        # Checks before adding to the database
        if not _functions.is_float(chapters_read) or len(chapters_read) == 0:
            messagebox.showerror("Input Error", "Invalid input for field 'chapters_read'")
            return

        new_data = {
            "title": _functions.remove_nasty_chars(self.input_widgets["title"].get()),
            "url": self.input_widgets["url"].get(),
            "chapters_read": self.input_widgets["chapters_read"].get(),
            "status": MangaStatusEnum.str_to_int(self.input_widgets["status"].get())
        }

        row_updated = database_queries.manga_update_with_id(self.manga_data.id, **new_data)

        if not row_updated:
            messagebox.showerror("Database Error", "Row failed to update")
            return

        self.destroy()
        self.callback()

    def delete_callback(self):
        if messagebox.askyesno("Delete Row", f"Remove {self.manga_data.title} from database?"):
            database_queries.manga_delete_with_id(self.manga_data.id)

            self.callback()
            self.destroy()

    def latest_offline_callback(self, event=None):
        remove_zero = _functions.remove_trailing_zeros_if_zero

        self.input_widgets["chapters_read"].set_text(remove_zero(self.manga_data.latest_chapter))
