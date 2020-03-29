import webbrowser
import manganelo
import threading
import time

from . import (RootWindow, Treeview, Combobox, SearchWindow)

import functools as ft

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox

from src.common import mangastatus
from src.database import DBConnection


class TreeOptions(tk.Frame):
	def __init__(self, master=None, *, command=None):
		super(TreeOptions, self).__init__(master, relief=tk.RAISED, borderwidth=1)

		self.vars = dict(updates_only=tk.BooleanVar())

		for text, var in (("Updates Only", "updates_only"),):
			c = tk.Checkbutton(self, text=text, variable=self.vars.get(var))

			c.config(command=command)

			c.pack(side=tk.LEFT)


class Toolbar(tk.Frame):
	def __init__(self, master=None):
		super(Toolbar, self).__init__(master, relief=tk.RAISED, borderwidth=1)

		self.search_entry = ttk.Entry(self)
		self.search_btn = ttk.Button(self, text="Search")
		self.status_combo = Combobox(self, mangastatus.all_text())

		self.status_combo.pack(side=tk.LEFT, padx=5, pady=5)
		self.search_btn.pack(side=tk.RIGHT, padx=5, pady=5)
		self.search_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)


class CentralFrame(tk.Frame):
	TREE_HEADINGS = ["ID", "Title", "Chapters Read", "Latest Chapter"]

	def __init__(self, master=None):
		super(CentralFrame, self).__init__(master, relief=tk.RAISED)

		self.tree = Treeview(self, self.TREE_HEADINGS)

		self.tree.pack(fill=tk.BOTH, expand=True)


class Application(RootWindow):
	def __init__(self):
		super(Application, self).__init__("Manga Tracker", geometry="750x400")

		self.current_status = mangastatus.index2status(0)

		# - Create UI
		self.toolbar = Toolbar(self)
		self.options = TreeOptions(self, command=self.on_options_change)
		self.central = CentralFrame(self)

		self.create_menu()

		# - Assign callbacks
		self.toolbar.status_combo.config(command=self.on_status_combo_change)
		self.toolbar.search_btn.config(command=ft.partial(self.on_search_button, self.toolbar.search_btn))

		# - Initial Method Calls
		self.update_tree()

		# - Widget placements
		self.toolbar.pack(fill=tk.X, padx=5, pady=5)
		self.options.pack(fill=tk.X, padx=5, pady=5)
		self.central.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

	def create_menu(self):
		menu = tk.Menu(self.central.tree, tearoff=0)

		menu.add_command(label="Open in Browser", command=self.open_in_browser)

		menu.master.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

	def update_tree(self):
		self.central.tree.clear()

		with DBConnection() as con:
			query = con.get_query("selecttreemanga.sql")
			if query is not None:
				con.cur.execute(query, (self.current_status.id,))
				results = con.cur.fetchall()

		results = self.apply_tree_options(self.options.vars, results)

		self.central.tree.populate(results)

	@staticmethod
	def apply_tree_options(var_dict, data):
		if var_dict.get("updates_only").get():
			data = list(filter(lambda row: row.latest_chapter > row.chapters_read, data))

		return data

	@staticmethod
	def open_in_browser(url):
		if url is not None:
			webbrowser.open(url, new=True)
		else:
			messagebox.showerror("URL could not be opened", f"'{url}' could not be opened.")

	def on_open_in_browser(self):
		row = self.central.tree.one()

		if row is not None:
			with DBConnection() as con:
				query = con.get_query("url.sql")

				if query is not None:
					con.cur.execute(query, (row[0],))
					result = con.cur.fetchone()

		self.open_in_browser(result.url)

	def on_options_change(self):
		self.after(50, self.update_tree)

	def on_status_combo_change(self, event):
		self.current_status = mangastatus.index2status(event.widget.val_index)
		self.update_tree()

	def on_search_button(self, btn):
		def predicate():
			btn.state(["!disabled"])
			#btn.after(100, predicate)

		btn.state(["disabled"])

		predicate()

