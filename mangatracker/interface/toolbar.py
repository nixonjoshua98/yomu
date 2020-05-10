import tkinter as tk

from mangatracker.interface.combobox import Combobox


class Toolbar(tk.Frame):
    def __init__(self, master=None):
        super(Toolbar, self).__init__(master=master)

        self.combo = Combobox(self, [0, 1, 2, 3])

        self.combo.pack(side=tk.LEFT)