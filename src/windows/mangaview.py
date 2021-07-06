import ast

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox

from src import storage, statuses

from src.widgets import ChildWindow, ComboBox


class MangaView(ChildWindow):
	def __init__(self, iid):
		super().__init__()

		self._document_iid = iid

		self.values = storage.get().find_one(self._document_iid)

		self.widgets = dict()
		self.frame = None

		self._configure_window()

	def _configure_window(self):
		self.resizable(0, 0)

		self.center_in_root(400, 250)

		self.create()

		self.show()

	def create(self):
		self.frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		self.widgets["title"] = self.create_entry("Title", default=self.values["title"])
		self.widgets["url"] = self.create_entry("Url", default=self.values["url"])

		self.widgets["chapters_read"] = self.create_entry_with_button(
			"Chapters Read",
			default=self.values["chapters_read"],
			text="Latest",
			command=self.on_latest
		)

		self.widgets["status"] = self.create_combo("Reading Status", values=statuses.all_text)
		self.widgets["status"].current(self.values["status"])

		b = ttk.Button(self.frame, text="Confirm", command=self.on_confirm)
		b.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

		b = ttk.Button(self.frame, text="Undo", command=self.on_undo)
		b.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

		b = ttk.Button(self.frame, text="Delete", command=self.on_delete)
		b.pack(fill=tk.X, side=tk.LEFT, pady=5, padx=5, expand=True)

		self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

	def on_confirm(self):

		try:
			chapters_read = ast.literal_eval(self.widgets["chapters_read"].get())
		except ValueError:
			return messagebox.showerror("Value Error", "Value must be an integer or float.")

		status = statuses.text_to_id(self.widgets["status"].get())

		self._update_document(status, chapters_read)

		self.master.update_tree()

		self.destroy()

	def on_undo(self):
		children = tuple(self.children.values())

		for child in children:
			child.destroy()

		self._configure_window()

	def on_delete(self):
		storage.get().delete_one(self._document_iid)

		self.destroy()

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

	def _update_document(self, status, chapters_read):

		storage.get().update_one(
			self._document_iid,
			{
				"title": self.widgets["title"].get(),
				"url": self.widgets["url"].get(),
				"status": status,
				"chapters_read": chapters_read
			}
		)