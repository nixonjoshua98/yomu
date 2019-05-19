import tkinter as tk

# Sometimes messagebox cannot be imported
# bringing it into the file 'as' a name fixes this issue
from tkinter import messagebox as tkMsgBox


class ChildWindow(tk.Toplevel):
    def __init__(self, title: str, resize: bool = True, geometry: str = None, destroy_on_exit: bool = True):

        super().__init__()

        self.is_viewable = False

        self.title(title)
        self.resizable(resize, resize)

        if geometry:
            self.geometry(geometry)
        
        if destroy_on_exit:
            self.protocol("WM_DELETE_WINDOW", self.destroy)
        else:
            self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def show_window(self):
        self.is_viewable = True
        self.deiconify()

    def hide_window(self):
        self.is_viewable = False
        self.withdraw()

    def toggle_view(self):
        if self.is_viewable:
            self.hide_window()
        else:
            self.show_window()
