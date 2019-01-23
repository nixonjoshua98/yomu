import tkinter as tk

from tkinter import ttk

from interface.widgets.treeView import TreeView

class DownloadQueueFrame(tk.Frame):
    def __init__(self, master, downloadManager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.downloadmanager = downloadManager

        self.treeView = TreeView(self, ["Comic Title", "Chapter No."], [500])

        self.updateTree()

        self.treeView.pack(fill = tk.BOTH, expand = True)

    def updateTree(self, event = None):
        if (len(self.downloadmanager.queue) > 0):
            self.treeView.insertData([self.downloadmanager.queue.pop(0)], reversed = True)

        try:
            self.master.after(1000, self.updateTree)
        except Exception:
            """ Window was most likely destroyed """

