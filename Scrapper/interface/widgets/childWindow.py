import tkinter as tk

from tkinter import messagebox as tkMsgBox

class ChildWindow(tk.Toplevel):
    def __init__(self, title, geometry, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onWindowClose)

    def onWindowClose(self):
        self.destroy()
