import webbrowser

import manganelo.rewrite as manganelo

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

import functools as ft

from src import utils, storage, statuses

from src.widgets import Treeview, ComboBox
from src.windows import MangaView, SearchView


class Application(tk.Tk):
	def __init__(self):
		super(Application, self).__init__()

		self._configure_window()

		self.tree = None
		self.tree_data = list()
		self.combo_val = None

		self.filters = {"readable_only": tk.BooleanVar(value=True)}

		self.create()

		self.update_tree()

	def _configure_window(self):
		self.wm_title("Manga")
		self.geometry("800x400")
		self.resizable(0, 0)

	def create(self):
		""" Create the windows widgets. """

		# - - - Tool Bar - - - #
		frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		combo = ComboBox(frame, values=statuses.all_text, command=self.on_status_change)
		combo.pack(side=tk.LEFT, padx=5, pady=5)

		search_entry = ttk.Entry(frame)
		search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

		search_btn = ttk.Button(frame, text="Search")
		search_btn.config(command=ft.partial(self.on_search_btn, search_btn, search_entry))
		search_btn.pack(side=tk.LEFT, padx=5, pady=5)

		frame.pack(fill=tk.X, padx=5, pady=5)

		# - - - Filter Menu - - - #
		frame = tk.Frame(self)

		c = tk.Checkbutton(
			frame,
			text="Readable",
			variable=self.filters["readable_only"],
			command=self.on_filter_update
		)

		c.pack(side=tk.LEFT)

		frame.pack(fill=tk.X, padx=5)

		# - - - Treeview - - - #
		frame = tk.Frame(self)

		self.tree = Treeview(
			frame,
			headings=["Title", "Chapter Read", "Latest Chapter"],
			widths=[500, 125, 125]
		)

		self.tree.bind("<Double-1>", self.on_row_select)

		self.tree.pack(fill=tk.BOTH, expand=True)

		frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		# - - - Menu - - - #
		menu = tk.Menu(self.tree, tearoff=0)

		menu.add_command(label="Open in Browser", command=self.open_in_browser)

		self.tree.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

		# - - - Attributes - - - #
		self.combo_val = combo.get()

	def update_tree(self):

		def to_list(d):
			return [d[k] for k in ("mangaId", "title", "chapters_read", "latest_chapter")]

		self.tree_data = storage.get_instance().get_with_status(
			statuses.text_to_id(self.combo_val),
			readable_only=self.filters["readable_only"].get()
		)

		self.tree_data.reverse()

		self.tree.populate(map(to_list, self.tree_data))

	def open_in_browser(self):
		if iid := self.tree.focus():
			row = storage.get_instance().find_one(iid)

			webbrowser.open(row["url"], new=False)

	@staticmethod
	def on_row_select(event):
		if iid := event.widget.focus():
			MangaView(iid)

	def on_search_btn(self, btn, entry: ttk.Entry):

		# Refuse to search
		if len(query := entry.get()) < 3:
			return messagebox.showerror("Search Query", "Search query is too short.")

		def callback(results):
			btn.state(["!disabled"])

			SearchView(results)

		btn.state(["disabled"])

		utils.run_in_pool(ft.partial(manganelo.search, title=query), ft.partial(self.after, 0, callback))

	def on_status_change(self, event):
		self.combo_val = event.widget.get()

		self.update_tree()

	def on_filter_update(self):
		self.update_tree()
