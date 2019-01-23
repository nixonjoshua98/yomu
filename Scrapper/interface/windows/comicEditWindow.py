import tkinter as tk

from tkinter import ttk

from interface.widgets.comboBox    import ComboBox
from interface.windows.childWindow import ChildWindow

import functions.functions as funcs

# Static class
from classes.comicStatus import ComicStatus

class ComicEditWindow(ChildWindow):
    def __init__(self, comicTitle, chaptersRead, comicStatusIndex, exitCommand):
        super().__init__(comicTitle, "1x1")

        # Grabbing x and y of master
        position = self._nametowidget(self.winfo_parent()).geometry().split("+")
        x, y = position[1], position[2]

        self.geometry("350x200+%s+%s" % (x, y))


        
        self.chaptersRead     = chaptersRead
        self.comicTitle       = comicTitle
        self.comicStatusIndex = comicStatusIndex
        self.exitCommand      = exitCommand

        ttk.Style().configure("White.Label", background = "#ffffff")

        self.mainFrame         = tk.Frame(self,           bg = "#ffffff")
        self.chaptersReadFrame = tk.Frame(self.mainFrame, bg = "#ffffff")
        self.comicStatusFrame  = tk.Frame(self.mainFrame, bg = "#ffffff")

        self.titleLbl           = ttk.Label (master = self.mainFrame,         text = "Update Record", style = "White.Label", font = ("Ariel", 15))
        self.chaptersReadLbl    = ttk.Label (master = self.chaptersReadFrame, text = "Chapters Read", style = "White.Label")
        self.comicStatusLbl     = ttk.Label (master = self.comicStatusFrame,  text = "Comic Status", style = "White.Label")

        self.chaptersReadAllBtn = ttk.Button(master = self.chaptersReadFrame, text = "Read All", command = self.readAllChapters)
        self.confirmBtn         = ttk.Button(master = self.mainFrame,         text = "Confirm",  command = self.confirmChanges)
        self.resetBtn           = ttk.Button(master = self.mainFrame,         text = "Undo",     command = self.resetToDefault)

        self.chaptersReadEntry  = ttk.Entry (master = self.chaptersReadFrame, width = 20)

        self.comicStatusCombo   = ComboBox(self.comicStatusFrame, ComicStatus.allText(), None)

        self.bind("<Return>", self.confirmChanges)

        self.titleLbl.pack(pady = 15)
        
        self.chaptersReadLbl.pack       (side = tk.LEFT, padx = 15)
        self.chaptersReadEntry.pack     (side = tk.LEFT, padx = 15)
        self.chaptersReadAllBtn.pack    (padx = 15)
        
        self.comicStatusLbl.pack   (side = tk.LEFT,  padx = 15)
        self.comicStatusCombo.pack (side = tk.RIGHT, padx = 20)
        
        self.mainFrame.pack        (expand = True, fill = tk.BOTH)
        self.chaptersReadFrame.pack(anchor = tk.W, pady = 10)
        self.comicStatusFrame.pack (anchor = tk.W, pady = 10)

        self.confirmBtn.pack(side = tk.LEFT,  padx = 30)
        self.resetBtn.pack  (side = tk.RIGHT, padx = 30)

        self.chaptersReadEntry.focus()
        self.resetToDefault()

    def resetToDefault(self, event = None):
        self.chaptersReadEntry.delete(0, "end")
        self.chaptersReadEntry.insert(0, self.chaptersRead)
        self.comicStatusCombo.current(self.comicStatusIndex)

    def readAllChapters(self, event = None):
        latestChap = funcs.getLatestChapter(self.comicTitle)
        self.chaptersReadEntry.delete(0, "end")
        self.chaptersReadEntry.insert(tk.END, latestChap)

    def confirmChanges(self, event = None):
        self.exitCommand(self)
        self.onWindowClose()

    def getChaptersRead(self, event = None):
        return funcs.parseToNumber(self.chaptersReadEntry.get())

    def getComicStatus(self):
        return ComicStatus.textToId(self.comicStatusCombo.get())

    def getComicTitle(self):
        return self.comicTitle
