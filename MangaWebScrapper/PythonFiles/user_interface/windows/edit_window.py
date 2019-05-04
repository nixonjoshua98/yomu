import tkinter as tk
import tkinter.ttk as ttk

import user_interface.widgets as widgets

from database.database_models import Manga

from database.database_functions import (
    get_table_pk,
    get_enums_from_enum_field,
)


class MangaEditWindow(widgets.ChildWindow):
    def __init__(self, manga_data: Manga):
        super().__init__(manga_data.title, resize=True, destroy_on_exit=True)

        # - Frames
        root_frame = ttk.Frame(self)

        # Loop over the fields
        for table_field in Manga.__table__.columns.keys():
            row_frame = tk.Frame(root_frame)

            lbl = tk.Label(row_frame, text=table_field.title().replace("_", " "))

            enums = get_enums_from_enum_field(Manga, table_field)

            # If not an enum field type
            if not enums:
                entry = ttk.Entry(row_frame)

                entry.insert(0, getattr(manga_data, table_field))

                entry.pack(side=tk.RIGHT, fill=tk.X, padx=5, expand=True)

                # Catch the primary key to disable it
                if get_table_pk(Manga) is table_field:
                    entry.state(["disabled"])

            # Enum field
            else:
                dropdown = widgets.Dropdown(row_frame, [e.title().replace("_", " ") for e in enums], lambda: print())

                dropdown.pack(side=tk.RIGHT, fill=tk.X, padx=5, expand=True)

            lbl.pack(side=tk.LEFT, padx=5, fill=tk.X)
            row_frame.pack(fill=tk.X, pady=5)

        confirm_btn = ttk.Button(root_frame, text="Confirm")
        undo_btn = ttk.Button(root_frame, text="Undo")

        # - Placements
        root_frame.pack(fill=tk.X)
        confirm_btn.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)
        undo_btn.pack(fill=tk.X, side=tk.RIGHT, pady=5, padx=5, expand=True)
