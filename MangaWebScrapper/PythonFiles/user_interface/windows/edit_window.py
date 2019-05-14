import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox as tkMsgBox

import user_interface.widgets as widgets

from database.database_models import Manga
import database.database_queries as queries

from database.database_enums import (
    MangaStatusEnum
)

from functions.functions import (
    remove_trailing_zeros_if_zero,
    is_float
)


class MangaEditWindow(widgets.ChildWindow):
    def __init__(self, manga_data: Manga, success_callback):
        super().__init__(manga_data.title, resize=True, destroy_on_exit=True)

        self.manga_data = manga_data
        self.input_widgets = {}
        self.on_success_callback = success_callback

        # - Frames
        self.root_frame = ttk.Frame(self)

        self.create_field_inputs()

        # - Default Buttons
        confirm_btn = ttk.Button(self.root_frame, text="Confirm", command=self.confirm_callback)
        undo_btn = ttk.Button(self.root_frame, text="Undo", command=self.undo_callback)

        # - Placements
        self.root_frame.pack(fill=tk.X)
        confirm_btn.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)
        undo_btn.pack(fill=tk.X, side=tk.RIGHT, pady=5, padx=5, expand=True)

    def create_entry(self, parent, default_text, disabled=False) -> widgets.EntryField:
        entry = widgets.EntryField(parent)
        entry.set_text(default_text)

        if disabled:
            entry.state(["disabled"])

        entry.pack(side=tk.RIGHT, fill=tk.X, padx=5, expand=True)

        return entry

    def create_dropdown(self, parent, values, initial_value_index) -> widgets.Dropdown:
        dropdown = widgets.Dropdown(parent, values, lambda: print())

        dropdown.current(initial_value_index)

        dropdown.pack(side=tk.RIGHT, fill=tk.X, padx=5, expand=True)

        return dropdown

    def create_field_inputs(self):
        # - ID (PK)
        row_frame = tk.Frame(self.root_frame)
        lbl = tk.Label(row_frame, text="Manga ID")
        self.input_widgets["id"] = self.create_entry(row_frame, self.manga_data.id, disabled=True)

        lbl.pack(side=tk.LEFT, padx=5, fill=tk.X)
        row_frame.pack(fill=tk.X, pady=5)

        # - Title
        row_frame = tk.Frame(self.root_frame)
        lbl = tk.Label(row_frame, text="Title")
        self.input_widgets["title"] = self.create_entry(row_frame, self.manga_data.title, disabled=True)

        lbl.pack(side=tk.LEFT, padx=5, fill=tk.X)
        row_frame.pack(fill=tk.X, pady=5)

        # - Menu URL
        row_frame = tk.Frame(self.root_frame)
        lbl = tk.Label(row_frame, text="Menu URL")
        self.input_widgets["menu_url"] = self.create_entry(row_frame, self.manga_data.menu_url)

        lbl.pack(side=tk.LEFT, padx=5, fill=tk.X)
        row_frame.pack(fill=tk.X, pady=5)

        # - Chapters Read
        row_frame = tk.Frame(self.root_frame)
        lbl = tk.Label(row_frame, text="Chapters Read")

        default_val = remove_trailing_zeros_if_zero(self.manga_data.chapters_read)

        self.input_widgets["chapters_read"] = self.create_entry(row_frame, default_val)

        lbl.pack(side=tk.LEFT, padx=5, fill=tk.X)
        row_frame.pack(fill=tk.X, pady=5)

        # - Manga Status
        row_frame = tk.Frame(self.root_frame)
        lbl = tk.Label(row_frame, text="Status")

        initial_val_index = MangaStatusEnum(self.manga_data.status).value
        all_values = [e.formatted_name for e in MangaStatusEnum]

        self.input_widgets["status"] = self.create_dropdown(row_frame, all_values, initial_val_index)

        lbl.pack(side=tk.LEFT, padx=5, fill=tk.X)
        row_frame.pack(fill=tk.X, pady=5)

    def undo_callback(self, event=None):
        self.input_widgets["title"].set_text(self.manga_data.title)
        self.input_widgets["menu_url"].set_text(self.manga_data.menu_url)
        self.input_widgets["chapters_read"].set_text(self.manga_data.chapters_read)
        self.input_widgets["status"].current(MangaStatusEnum(self.manga_data.status).value)

    def confirm_callback(self, event=None):
        chapters_read = self.input_widgets["chapters_read"].get()
        if not is_float(chapters_read):
            tkMsgBox.showerror("Input Error", "Invalid datatype for field 'chapters_read'")
            return

        print(MangaStatusEnum.formatted_name2int(self.input_widgets["status"].get()))

        new_data = {
            "title": self.input_widgets["title"].get(),
            "menu_url": self.input_widgets["menu_url"].get(),
            "chapters_read": self.input_widgets["chapters_read"].get(),
            "status": MangaStatusEnum.formatted_name2int(self.input_widgets["status"].get())
        }

        queries.manga_update_with_id(self.manga_data.id, **new_data)

        self.destroy()

        self.on_success_callback()
