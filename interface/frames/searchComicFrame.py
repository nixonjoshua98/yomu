import threading

import tkinter as tk

from tkinter import ttk

from tkinter import messagebox as tkMsgBox

from classes.database import Database

from interface.widgets.treeView import TreeView

from manganelo.searchComic import SearchComic

class SearchComicFrame(tk.Frame):
    def __init__(self, master, searchBtn, searchEntry, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master      = master
        self.searchBtn   = searchBtn
        self.searchEntry = searchEntry

        self.searchThread  = None
        self.searchResults = None

        self.treeView = TreeView(self, ["Comic Title", "Latest Chapter"], [350])

        self.rightClickMenu = tk.Menu(self.treeView, tearoff = 0)
        self.rightClickMenu.add_command(label = "Add to Database", command = self.addComic)

        self.treeView.bind("<Button-3>", self.onRightClick)

        self.treeView.pack(fill = tk.BOTH, expand = True)

    def onRightClick(self, event = None):
        if len((self.treeView.getSelected())) >= 1:
            self.rightClickMenu.post(event.x_root, event.y_root)

    def addComic(self, event = None):
        rowSelected = self.treeView.getSelected()
        if (not Database.comicExists(rowSelected[0])):
            Database.addRow(rowSelected[0], rowSelected[2], rowSelected[3])
        else:
            tkMsgBox.showinfo("Comic Exists", "Cannot add comic to database")
            

    def search(self, start = True):
        if (start):
            if (len(self.searchEntry.get().replace(" ", "")) >= 3):
                self.searchThread = threading.Thread(target = self.searchThreadFunc)
                self.searchThread.start()
            else:
                return -1

        elif (not start):
            if (self.searchResults != None):
                self.treeView.clearData()
                self.treeView.insertData(self.searchResults)
                self.searchResults = None
                return 0
            
        self.master.after(500, lambda: self.search(False))
        

    def searchThreadFunc(self):
        self.searchBtn.state(["disabled"])
        self.searchResults = SearchComic(self.searchEntry.get())
        self.searchBtn.state(["!disabled"])

