import functools as ft
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import webbrowser
from typing import Optional

from src import utils
from src.app_config import AppConfig
from src.combobox import ComboBox
from src.data_entities import Story
from src.data_repository import DataRepository
from src.editwindow import StoryEditWindow
from src.email_util import send_email
from src.search_result_window import SearchResultWindow
from src.statuses import StatusList
from src.table import Table


class Application(tk.Tk):
    def __init__(self, config: AppConfig, repository: DataRepository):
        super(Application, self).__init__()

        self.repository = repository
        self.config = config

        self._configure_window()

        self.tree = None
        self.tree_data = list()

        self.status_combo: Optional[ComboBox] = None

        self.filters = {"readable_only": tk.BooleanVar(value=True)}

        self.create()

        self.update_tree()

    @property
    def current_status(self):
        return self.status_combo.current_value

    def _configure_window(self):
        self.wm_title("Yomu")
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

        self.tree.bind("<Button-3>", self._post_context_menu)

    def _post_context_menu(self, e):
        iid = self.tree.focus()

        if iid == "" or (story := self.repository.get(iid)) is None:
            return

        menu = self._create_context_menu(self.tree, story)

        menu.post(e.x_root, e.y_root)

    def _create_context_menu(self, parent, story: Story) -> tk.Menu:
        menu = tk.Menu(parent, tearoff=0)

        menu.add_command(label="Open in Browser", command=lambda : self._open_story_url(story))

        if story.has_unread_chapter:
            menu.add_command(label="Mark as read", command=lambda: self._read_story(story))

        return menu

    def update_tree(self):
        def to_list(s: Story) -> tuple:
            return (
                s.id,
                s.title,
                utils.format_number(s.latest_chapter_read),
                utils.format_number(s.latest_chapter),
            )

        self.tree_data = self.repository.get_stories_with_status(
            self.current_status, readable_only=self.filters["readable_only"].get()
        )

        self.tree.populate(map(to_list, self.tree_data))

    @staticmethod
    def _open_story_url(story: Story):
        webbrowser.open(story.url, new=False)

    def _read_story(self, story: Story):
        story.latest_chapter_read = story.latest_chapter
        self.repository.update(story)
        self.update_tree()

    def on_dump_button_pressed(self):
        ls = self.repository.get_readable_stories()

        ls = [f"[{x.latest_chapter_read} / {x.latest_chapter}] {x.title}\n{x.url}" for x in ls]

        send_email(
            "Yomu Story Dump",
            self.config.email_sender.email_address,
            self.config.email_receiver,
            self.config.email_sender.password,
            "\n\n".join(ls),
        )

    def on_row_select(self, event):
        if iid := event.widget.focus():
            StoryEditWindow(iid, self.repository)

    def on_search_btn(self, entry: ttk.Entry):

        if len(query := entry.get()) < 3:
            return messagebox.showerror("Search Query", "Search query is too short.")

        SearchResultWindow(query, self.repository)
