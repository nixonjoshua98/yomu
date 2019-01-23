import sys

import tkinter as tk

from tkinter import messagebox as tkMsgBox


class RootWindow(tk.Tk):    
    def __init__(self, title, geometry, onCloseCommands = []):
        super().__init__()

        self.onCloseCommands = onCloseCommands

        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onWindowClose)

    def onWindowClose(self):
        closeWindow = tkMsgBox.askyesno("Exit Application", "Are you sure?")
        
        if (closeWindow):
            self.destroy()
            self.quit()

            for command in self.onCloseCommands:
                command()

            sys.exit(0)
