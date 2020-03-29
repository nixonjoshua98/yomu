import tkinter as tk


class RootWindow(tk.Tk):

	def __init__(self, title, *, geometry=None):
		super().__init__()

		self.title(title)

		if geometry is not None:
			self.geometry(geometry)

		self.protocol("WM_DELETE_WINDOW", self.on_close)

	def on_close(self):
		self.destroy()
		self.quit()

