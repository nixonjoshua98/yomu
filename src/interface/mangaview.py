import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox

from src.statuses import Statuses

from .widgets import ComboBox
from .childwindow import ChildWindow


class MangaView(ChildWindow):
	def __init__(self, *, values: dict, database):
		super().__init__()

		# Window Configuration
		self.resizable(0, 0)

		self.values = values
		self.database = database

		self.widgets = dict()
		self.frame: tk.Frame = None

		self.create()

		self.center_in_root(400, 250)

		self.show()

	def create(self):
		self.frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		self.widgets["title"] = self.create_entry("Title", default=self.values["title"])
		self.widgets["url"] = self.create_entry("Menu URL", default=self.values["url"])

		self.widgets["chapters_read"] = self.create_entry_with_button(
			"Chapters Read",
			default=self.values["chapters_read"],
			text="Latest",
			command=self.on_latest
		)

		self.widgets["status"] = self.create_combo("Reading Status", values=Statuses.all_text)
		self.widgets["status"].current(Statuses.index(id=self.values["status"]))

		b = ttk.Button(self.frame, text="Confirm", command=self.on_confirm)
		b.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

		b = ttk.Button(self.frame, text="Undo", command=self.on_undo)
		b.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

		b = ttk.Button(self.frame, text="Delete", command=self.on_delete)
		b.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

		self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

	def on_confirm(self):
		chapters_read = self.widgets["chapters_read"].get()

		try:
			chapters_read = float(chapters_read)
		except ValueError:
			messagebox.showerror("Chapters Read", "Value must be an integer or float.")

		status = Statuses.get(text=self.widgets["status"].get())["id"]

		self.database.manga.update(
			{"_id": self.values["_id"]},
			{
				"$set":
					{
						"title": self.widgets["title"].get(),
						"url": self.widgets["url"].get(),
						"status": status,
						"chapters_read": chapters_read
					},
			}
		)

		self.master.update_tree()
		self.destroy()

	def on_undo(self):
		children = tuple(self.children.values())

		for child in children:
			child.destroy()

		self.create()

	def on_delete(self):
		pass

	def on_latest(self):
		w = self.widgets["chapters_read"]

		w.delete(0, tk.END)
		w.insert(0, self.values["latest_chapter"])

	def create_entry(self, title, *, default):
		entry = self._create_label_widget_combo(title, widget=ttk.Entry)

		entry.insert(0, default)

		return entry

	def create_entry_with_button(self, title, *, default, text, command):
		entry = self._create_label_widget_combo(title, widget=ttk.Entry)

		btn = ttk.Button(entry.master, text=text, command=command)

		btn.pack(side=tk.LEFT)

		entry.insert(0, default)

		return entry

	def create_combo(self, title, *, values):
		return self._create_label_widget_combo(title, widget=ComboBox, values=values)

	def _create_label_widget_combo(self, title, *, widget, **kwargs):
		label_frame = tk.Frame(self.frame)
		widget_frame = tk.Frame(self.frame)

		lbl = tk.Label(label_frame, text=title)
		lbl.pack(side=tk.LEFT, fill=tk.X)

		label_frame.pack(fill=tk.BOTH)
		widget_frame.pack(fill=tk.BOTH)

		widget_inst = widget(widget_frame, **kwargs)
		widget_inst.pack(side=tk.LEFT, fill=tk.X, padx=5, expand=True)

		return widget_inst