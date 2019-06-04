import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox

import functions
import constants
import database.enums
import database.queries

import user_interface.widgets as widgets


class MangaEditWindow(widgets.ChildWindow):
    def __init__(self, manga_data, success_callback):
        super().__init__(manga_data.title, resize=False, destroy_on_exit=True)

        self.manga_data = manga_data
        self.input_widgets = {}
        self.callback = success_callback

        # - Frames
        self.root_frame = ttk.Frame(self)

        self.create_field_inputs()

        # - Default Buttons
        ttk.Button(self.root_frame, text="Confirm", command=self.confirm_callback)\
            .pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

        ttk.Button(self.root_frame, text="Undo", command=self.undo_callback)\
            .pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

        ttk.Button(self.root_frame, text="Delete", command=self.delete_callback)\
            .pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

        self.bind("<Return>", self.confirm_callback)

        self.root_frame.pack(fill=tk.X)

    def create_dropdown(self, widget_key, label_text, initial_index, values) -> widgets.Dropdown:
        lbl_frame = tk.Frame(self.root_frame)
        drop_frame = tk.Frame(self.root_frame)
        dropdown = widgets.Dropdown(drop_frame, values)

        tk.Label(lbl_frame, text=label_text).pack(side=tk.LEFT, fill=tk.X)

        dropdown.current(initial_index)

        self.input_widgets[widget_key] = dropdown

        lbl_frame.pack(fill=tk.X, pady=5)
        drop_frame.pack(fill=tk.X)
        dropdown.pack(side=tk.RIGHT, fill=tk.X, padx=5, expand=True)

    def create_entry(self, widget_key, label_text, initial_val, disabled=False, focus=False) -> tk.Frame:
        lbl_frame = tk.Frame(self.root_frame)
        entry_frame = tk.Frame(self.root_frame)
        entry = widgets.EntryField(entry_frame)

        entry.set_text(initial_val)

        if disabled:
            entry.state(["disabled"])

        if focus:
            entry.focus_set()

        tk.Label(lbl_frame, text=label_text).pack(side=tk.LEFT, fill=tk.X)

        self.input_widgets[widget_key] = entry

        lbl_frame.pack(fill=tk.X, pady=5)
        entry_frame.pack(fill=tk.X)
        entry.pack(side=tk.LEFT, fill=tk.X, padx=5, expand=True)

        return entry_frame

    def create_field_inputs(self):
        # key, text, initial_val, disabled
        self.create_entry("id", "Manga ID", self.manga_data.id, disabled=True)
        self.create_entry("title", "Title", self.manga_data.title, disabled=True)
        self.create_entry("url", "Menu URL", self.manga_data.url)

        default_val = functions.remove_trailing_zeros_if_zero(self.manga_data.chapters_read)

        frame = self.create_entry("chapters_read", "Chapters Read", default_val, focus=True)

        ttk.Button(frame, text="Latest Chapter", command=self.latest_offline_callback).pack(side=tk.RIGHT, padx=5)

        initial_index = database.enums.MangaStatusEnum(self.manga_data.status).value

        self.create_dropdown("status", "Status", initial_index, constants.MANGA_STATUS)

    def undo_callback(self, event=None):
        chapters_read = functions.remove_trailing_zeros_if_zero(self.manga_data.chapters_read)

        self.input_widgets["title"].set_text(self.manga_data.title)
        self.input_widgets["url"].set_text(self.manga_data.url)
        self.input_widgets["chapters_read"].set_text(chapters_read)
        self.input_widgets["status"].current(database.enums.MangaStatusEnum(self.manga_data.status).value)

    def confirm_callback(self, event=None):
        chapters_read = self.input_widgets["chapters_read"].get()

        # Checks before adding to the database
        if not functions.is_float(chapters_read) or len(chapters_read) == 0:
            messagebox.showerror("Input Error", "Invalid input for field 'chapters_read'")
            return

        new_data = {
            "title": functions.remove_nasty_chars(self.input_widgets["title"].get()),
            "url": self.input_widgets["url"].get(),
            "chapters_read": self.input_widgets["chapters_read"].get(),
            "status": database.enums.MangaStatusEnum.str_to_int(self.input_widgets["status"].get())
        }

        row_updated = database.queries.manga_update_with_id(self.manga_data.id, **new_data)

        if not row_updated:
            messagebox.showerror("Database Error", "Row failed to update")
            return

        self.destroy()
        self.callback()

    def delete_callback(self):
        if messagebox.askyesno("Delete Row", f"Remove {self.manga_data.title} from database?"):
            database.queries.manga_delete_with_id(self.manga_data.id)

            self.callback()
            self.destroy()

    def latest_offline_callback(self, event=None):
        remove_zero = functions.remove_trailing_zeros_if_zero

        self.input_widgets["chapters_read"].set_text(remove_zero(self.manga_data.latest_chapter))
