import webbrowser

from . import (RootWindow, Treeview, Combobox)

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox

from src.common import mangastatus
from src.database import DBConnection


class Application(RootWindow):
	TREE_HEADINGS = ["ID", "Title", "Chapters Read", "Latest Chapter"]

	def __init__(self):
		super(Application, self).__init__("Manga Tracker", "750x400")

		self.current_status = mangastatus.index2status(0)
		self.options = dict(updates_only=tk.BooleanVar())

		self.tree = None

		self.create_toolbar()
		self.create_tree()
		self.create_menu()

	def create_toolbar(self):
		frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
		search_entry = ttk.Entry(frame)
		search_btn = ttk.Button(frame, text="Search", command=self.on_search_btn)
		status_combo = Combobox(frame, mangastatus.all_text(), command=self.on_status_combo_change)

		frame.pack(fill=tk.X, padx=5, pady=5)

		status_combo.pack(side=tk.LEFT, padx=5, pady=5)
		search_btn.pack(side=tk.RIGHT, padx=5, pady=5)
		search_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)

		frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)

		# Check Buttons
		check0 = tk.Checkbutton(
			frame,
			text="Updates Only",
			variable=self.options.get("updates_only"),
			command=self.on_options_change)

		check0.pack(side=tk.LEFT)
		# -

		frame.pack(fill=tk.X, padx=5)

	def create_tree(self):
		frame = tk.Frame(self, relief=tk.RAISED)
		self.tree = Treeview(frame, self.TREE_HEADINGS)

		self.update_tree()

		self.tree.pack(fill=tk.BOTH, expand=True)

		frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

	def create_menu(self):
		menu = tk.Menu(self.tree, tearoff=0)

		menu.add_command(label="Open in Browser", command=self.open_in_browser)

		menu.master.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

	# - - - LOGIC - - -

	def update_tree(self):
		self.tree.clear()

		with DBConnection() as con:
			query = con.get_query("selecttreemanga.sql")

			if query is not None:
				con.cur.execute(query, (self.current_status.id,))

				results = con.cur.fetchall()

		results = self.apply_tree_options(results)

		self.tree.populate(results)

	def apply_tree_options(self, data):
		if self.options.get("updates_only").get():
			data = list(filter(lambda row: row.latest_chapter > row.chapters_read, data))

		return data

	def open_in_browser(self):
		row = self.tree.one()

		if row is None:
			return

		with DBConnection() as con:
			query = con.get_query("selecturl.sql")
			if query is not None:
				con.cur.execute(query, (row[0],))
				result = con.cur.fetchone()

		if result is not None:
			webbrowser.open(result.url, new=True)
		else:
			messagebox.showerror("URL could not be opened", f"'{result.url}' could not be opened.")

	# - - - CALLBACKS - - -

	def on_options_change(self):
		def predicate():
			self.update_tree()

		self.after(50, predicate)  # Small delay to minimise the database calls when spamming

	def on_status_combo_change(self, event):
		self.current_status = mangastatus.index2status(event.widget.val_index)

		self.update_tree()

	def on_search_btn(self):
		pass
