import tkinter as tk

from tkinter import messagebox as tkMsgBox


class RootWindow(tk.Tk):
    """ Root window object, only one instance should ever be made at one time """
    def __init__(self, title, geometry):
        super().__init__()

        self.title(title)
        self.geometry(geometry)
        self.resizable(1, 1)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        close_window = tkMsgBox.askyesno("Exit Application", "Are you sure?")
        
        if close_window:
            self.destroy()
            self.quit()
