import ast
import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional

from src.childwindow import ChildWindow
from src.combobox import ComboBox
from src.entrybox import EntryBox
from src.models import Story
from src.statuses import StatusList
from src.storage import JSONStorage


class StoryEditWindow(ChildWindow):
    def __init__(self, story_data: Story, data_storage: JSONStorage):
        super().__init__()

        self._data_storage = data_storage
        self._story_data = story_data

        self._title: Optional[EntryBox] = None
        self._url: Optional[EntryBox] = None
        self._status: Optional[ComboBox] = None
        self._chapters_read: Optional[EntryBox] = None

        self._configure_window()

    @property
    def new_status(self):
        return self._status.current_value

    @property
    def new_chapters_read(self):
        return ast.literal_eval(self._chapters_read.get() or "0")

    @property
    def new_title(self):
        return self._title.get()

    @property
    def new_url(self):
        return self._url.get()

    def _configure_window(self):
        self.resizable(0, 0)

        self.center_in_root(400, 250)

        self.create()

        self.show()

    def destroy(self):
        self.master.update_tree()

        super(StoryEditWindow, self).destroy()

    def create(self):
        frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

        self._title = self._label_with_entry(frame, "Title", self._story_data.title)
        self._url = self._label_with_entry(frame, "Url", self._story_data.url)

        # = = Chapters Read = = #
        self._chapters_read = self._label_with_entry(
            frame, "Chapters Read", self._story_data.chapters_read, numbers_only=True
        )

        btn = ttk.Button(
            self._chapters_read.master, text="Latest", command=self.on_latest
        )
        btn.pack(side=tk.LEFT)

        # = = Reading Status = = #
        top_frame, btm_frame = self._vertical_frames(frame, 2)

        label = tk.Label(top_frame, text="Reading Status")
        label.pack(side=tk.LEFT, fill=tk.X)

        self._status = ComboBox(
            btm_frame,
            values=[[status.display_text, status.id] for status in StatusList],
            current=self._story_data.status_int,
        )
        self._status.pack(side=tk.LEFT, fill=tk.X, padx=5, expand=True)

        # = = Action Buttons = = #
        b = ttk.Button(frame, text="Confirm", command=self.on_confirm)
        b.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

        b = ttk.Button(frame, text="Undo", command=self.on_undo)
        b.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def on_confirm(self):
        self._update_document()

        self.destroy()

    def on_undo(self):
        children = tuple(self.children.values())

        for child in children:
            child.destroy()

        self._configure_window()

    def on_latest(self):
        self._chapters_read.set_text(self._story_data.latest_chapter)

    def _label_with_entry(self, master, label, text, numbers_only: bool = False):
        top_frame, btm_frame = self._vertical_frames(master, 2)

        label = tk.Label(top_frame, text=label)
        label.pack(side=tk.LEFT)

        entry = EntryBox(btm_frame, text=text, numbers_only=numbers_only)
        entry.pack(side=tk.LEFT, fill=tk.X, padx=5, expand=True)

        return entry

    @staticmethod
    def _vertical_frames(master, count: int = 2):
        main_frame = tk.Frame(master)

        frames = []
        for _ in range(count):
            frames.append(f := tk.Frame(main_frame))

            f.pack(fill=tk.X)

        main_frame.pack(fill=tk.X)

        return frames

    def _update_document(self):
        copy: Story = self._story_data.copy(deep=True)

        copy.title = self.new_title
        copy.url = self.new_url
        copy.status_int = self.new_status
        copy.chapters_read = self.new_chapters_read

        self._data_storage.update_one(copy)
