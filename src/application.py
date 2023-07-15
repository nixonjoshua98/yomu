import functools as ft
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import webbrowser
from typing import Optional

from src import storage, utils
from src.combobox import ComboBox
from src.editwindow import StoryEditWindow
from src.models import Story, AppConfig
from src.search_result_window import SearchResultWindow
from src.statuses import StatusList
from src.table import Table
from src.common.email_util import send_email


class Application(tk.Tk):
    def __init__(self, config: AppConfig):
        super(Application, self).__init__()

        self.config = config
        self.data_storage = storage.get_instance()

        self._configure_window()

        self.tree = None
        self.tree_data = list()

        # - - - Widgets - - - #
        self.status_combo: Optional[ComboBox] = None

        self.filters = {"readable_only": tk.BooleanVar(value=True)}

        self.create()

        self.update_tree()

    @property
    def current_status(self):
        return self.status_combo.current_value

    def _configure_window(self):
        self.wm_title("Manga")
        self.geometry("800x400")
        self.resizable(0, 0)

    def create(self):
        """Create the windows widgets."""

        # - - - Tool Bar - - - #
        frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

        self.status_combo = ComboBox(frame, command=lambda e: self.update_tree())
        self.status_combo.add_options(
            [[status.display_text, status.id] for status in StatusList]
        )
        self.status_combo.pack(side=tk.LEFT, padx=5, pady=5)

        search_entry = ttk.Entry(frame)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        search_btn = ttk.Button(frame, text="Search")
        search_btn.config(command=ft.partial(self.on_search_btn, search_entry))
        search_btn.pack(side=tk.LEFT, padx=5, pady=5)

        dump_btn = ttk.Button(frame, text="Dump", command=self.on_dump_button_pressed)
        dump_btn.pack(side=tk.LEFT, padx=5, pady=5)

        frame.pack(fill=tk.X, padx=5, pady=5)

        # - - - Filter Menu - - - #
        frame = tk.Frame(self)

        c = tk.Checkbutton(
            frame,
            text="Readable",
            variable=self.filters["readable_only"],
            command=self.update_tree,
        )

        c.pack(side=tk.LEFT)

        frame.pack(fill=tk.X, padx=5)

        # - - - Treeview - - - #
        frame = tk.Frame(self)

        self.tree = Table(
            frame,
            headings=["Title", "Chapter Read", "Latest Chapter"],
            widths=[500, 125, 125],
        )

        self.tree.bind("<Double-1>", self.on_row_select)

        self.tree.pack(fill=tk.BOTH, expand=True)

        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._create_context_menu()

    def _create_context_menu(self):
        menu = tk.Menu(self.tree, tearoff=0)

        menu.add_command(label="Open in Browser", command=self.open_in_browser)
        menu.add_command(label="Mark as read", command=self.mark_as_read)

        self.tree.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

    def update_tree(self):
        def to_list(s: Story) -> tuple:
            return s.id, s.title, utils.format_number(s.chapters_read), utils.format_number(s.latest_chapter)

        self.tree_data = self.data_storage.get_stories_with_status(
            self.current_status, readable_only=self.filters["readable_only"].get()
        )

        self.tree.populate(map(to_list, self.tree_data))

    def open_in_browser(self):
        if (iid := self.tree.focus()) and (story := self.data_storage.get_story(iid)):
            webbrowser.open(story.url, new=False)

    def mark_as_read(self):
        if not (iid := self.tree.focus()) or not (story := self.data_storage.get_story(iid)):
            return

        story.chapters_read = story.latest_chapter

        self.data_storage.update_story(story)

        self.update_tree()

    def on_dump_button_pressed(self):
        ls = self.data_storage.get_readable_stories()

        ls = [
            f"[{x.chapters_read} / {x.latest_chapter}] {x.title}\n{x.url}"
            for x in ls
        ]

        send_email(
            "Yomu Story Dump",
            self.config.email_sender.email_address,
            self.config.email_receiver,
            self.config.email_sender.password,
            "\n\n".join(ls)
        )

    def on_row_select(self, event):
        if iid := event.widget.focus():
            StoryEditWindow(self.data_storage.get_story(iid), self.data_storage)

    def on_search_btn(self, entry: ttk.Entry):

        if len(query := entry.get()) < 3:
            return messagebox.showerror("Search Query", "Search query is too short.")

        SearchResultWindow(query, self.data_storage)
