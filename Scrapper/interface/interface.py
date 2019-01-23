import tkinter as tk

from tkinter import ttk

import functions.functions as funcs

import enum

from interface.widgets.rootWindow import RootWindow

from interface.frames.toolBarFrame       import ToolBarFrame
from interface.frames.databaseViewFrame  import DatabaseViewFrame
from interface.frames.downloadQueueFrame import DownloadQueueFrame
from interface.frames.searchComicFrame   import SearchComicFrame

from classes.comicStatus     import ComicStatus # Static
from classes.comicSort       import ComicSort # Static
from classes.comicDataDict   import ComicDataDict
from classes.database        import Database # Static

class Interface(RootWindow):
    def __init__(self, downloadManager):
        super().__init__("Comic Tracker", "800x500", [downloadManager.stop])

        self.comicDataDict   = ComicDataDict()
        self.currentFrame    = 0
        self.currentSortId   = 1

        # ComboBox Widget Dictionaries
        comicStatusComboDict = {"values": ComicStatus.allViewabaleText(), "command": self.onComicStatusComboChange}

        changeTreeComboDict  = {"values": ["Database View", "Download Queue", "Comic Search"], "command": self.onChangeTreeComboChange}

        self.toolBarFrame       = ToolBarFrame(self, comicStatusComboDict, changeTreeComboDict, bg = "#d3d3d3")
        self.databaseViewFrame  = DatabaseViewFrame(self, self.toolBarFrame, self.onComicSortChange)
        self.downloadQueueFrame = DownloadQueueFrame(self, downloadManager, bg = "#ffffff")
        self.searchComicFrame   = SearchComicFrame(self, self.toolBarFrame.searchBtn, self.toolBarFrame.searchEntry)

        # Linked to the order of changeTreeComboDict["values"]
        self.mainFrames = [self.databaseViewFrame, self.downloadQueueFrame, self.searchComicFrame]

        # Adding button commands
        self.toolBarFrame.refreshBtn.config(command = self.onRefreshButtonClicked)
        self.toolBarFrame.searchBtn.config(command = self.onSearchBtnClicked)

        # Initial data etc...
        self.populateDatabaseView()

        # Place the widgets...
        self.toolBarFrame.pack(fill = tk.X)
        self.mainFrames[self.currentFrame].pack(fill = tk.BOTH, expand = True)


    # These two functions do the same thing, naming is easier to understand
    def onComicStatusComboChange(self, event = None):
        self.populateDatabaseView()

    def onComicSortChange(self, _id, event = None):
        self.currentSortId = _id
        self.populateDatabaseView()

    def onRefreshButtonClicked(self, event = None):
        self.refreshDataDict()
        self.populateDatabaseView()

    def onChangeTreeComboChange(self, event = None):
        self.switchFrame()

    def onSearchBtnClicked(self, event = None):
        self.searchComicFrame.search()

    def populateDatabaseView(self, _id = 0):
        comicStatusId = ComicStatus.textToId(self.toolBarFrame.comicStatusCombo.get())

        if (not self.comicDataDict.keyExists(comicStatusId)):
            self.refreshDataDict()

        # Get data, sort data and then display data
        data = self.comicDataDict.getValue(comicStatusId)
        sortedData = ComicSort.sort(data, self.currentSortId)
        self.databaseViewFrame.updateTreeView(sortedData)

    def refreshDataDict(self, event = None):
        comicStatusId = ComicStatus.textToId(self.toolBarFrame.comicStatusCombo.get())

        # Get data, add to data, update data
        newData = Database.getViewableComics(comicStatusId)
        data = [list(c) + [funcs.getAvailableChaps(*c)] for c in newData]
        self.comicDataDict.updateKey(comicStatusId, data)

    def switchFrame(self):
        newFrameIndex = self.toolBarFrame.changeTreeCombo.getIndex()

        newFrame = None

        for i, f in  enumerate(self.mainFrames):
            if (i == newFrameIndex):
                newFrame = f

            else:
                f.pack_forget()
        
        newFrame.pack(fill = tk.BOTH, expand = True)
