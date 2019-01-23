import sys

import tkinter as tk

from tkinter import messagebox as tkMsgBox


class RootWindow(tk.Tk):    
    """
    Function:
                __init__(self, title, geometry, onCloseCommand = [])
    Paramaters:
                title (str): Text which will be displayed at the very top of the window
                geometry(str): The geometry of the window using the format "WxH"
                onCloseCommands (Tuple/List of functions): Functions which will be called once the window has been destroyed
    Purpose:
                Class constructor, creates and initilises the object
    Returns:
                None
    """
    def __init__(self, title, geometry, onCloseCommands = []):
        super().__init__()

        self.onCloseCommands = onCloseCommands

        self.title(title)
        self.geometry(geometry)
        #self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onWindowClose)



    """
    Function:
                onWindowClose(self)
    Paramaters:
                None
    Purpose:
                Method is called once the quit button has been clicked on the window, it asks the user if they meant to exit and will call
                all of the [onCloseCommands]  which will be followed by a sys.exit(0)
    Returns:
                None
    """
    def onWindowClose(self):
        closeWindow = tkMsgBox.askyesno("Exit Application", "Are you sure?")
        
        if (closeWindow):
            self.destroy()
            self.quit()

            for command in self.onCloseCommands:
                command()

            sys.exit(0)
