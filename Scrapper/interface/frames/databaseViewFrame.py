import tkinter as tk
import functools as ft

from tkinter import ttk

import functions.functions as funcs

from classes.database import Database

from interface.widgets.treeView        import TreeView
from interface.windows.comicEditWindow import ComicEditWindow

from classes.comicSort import ComicSort # Static

class DatabaseViewFrame(tk.Frame):
    def __init__(self, master, toolBar, sortCommand, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master  = master
        self.toolBar = toolBar
        self.comicEditWindow = None

        self.treeView = TreeView(self, ["Comic Title", "Latest Chapter Read", "No. Chapters Available Offline"])

        # Creating the right click menu
        self.rightClickMenu = tk.Menu(self.treeView, tearoff = 0)        
        self.rightClickMenu.add_command(label = "Open in Explorer", command = self.openInExplorerCommand)
        self.rightClickMenu.add_command(label = "Edit Record",      command = self.editComicCommand)

        self.rightClickMenu.add_separator()

        # Sort menu (right click)
        self.sortMenu = tk.Menu(self.treeView, tearoff = 0)
        for t in ComicSort.allText():
            self.sortMenu.add_command(label = t, command = ft.partial(sortCommand, ComicSort.textToId(t)))

        self.rightClickMenu.add_cascade(label = "Sort by", menu = self.sortMenu)


        self.treeView.bind("<Button-3>", self.onRightClick)

        self.treeView.pack(fill = tk.BOTH, expand = True)

    def updateTreeView(self, data):
        self.treeView.clearData()
        self.treeView.insertData(data)

    def openInExplorerCommand(self, event = None):
        funcs.openComicInExplorer(self.treeView.getSelected()[0])

    def onRightClick(self, event):
        if (self.treeView.getSelected() != ""):
            self.rightClickMenu.post(event.x_root, event.y_root)

    def editComicCommand(self, event = None):
        if (self.comicEditWindow == None):
            values = self.treeView.getSelected()
            params = (values[0], funcs.parseToNumber(values[1]), self.toolBar.comicStatusCombo.getIndex(), self.updateComicInDatabase)
            self.comicEditWindow = ComicEditWindow(*params)
        else:
            self.comicEditWindow.onWindowClose()
            self.comicEditWindow = None
            self.editComicCommand()

    def updateComicInDatabase(self, event = None):
        cTitle  = self.comicEditWindow.getComicTitle()
        cStatus = self.comicEditWindow.getComicStatus()
        cRead   = self.comicEditWindow.getChaptersRead()
        Database.updateComic(cTitle, cStatus, cRead)
