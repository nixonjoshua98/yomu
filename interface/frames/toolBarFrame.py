import tkinter as tk

from tkinter import ttk

from interface.widgets.comboBox import ComboBox

class ToolBarFrame(tk.Frame):
    def __init__(self, master, comicStatusComboDict: dict, changeTreeComboDict: dict, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.comicStatusCombo = ComboBox(self, comicStatusComboDict["values"], comicStatusComboDict["command"])
        self.changeTreeCombo  = ComboBox(self,  changeTreeComboDict["values"],  changeTreeComboDict["command"], 5)

        self.searchEntry = ttk.Entry(self)

        self.refreshBtn = ttk.Button(self, text = "Refresh Data")
        self.searchBtn  = ttk.Button(self, text = "Search Online")

        self.comicStatusCombo.pack(side = tk.LEFT, pady = 3, padx = 3)
        self.refreshBtn.pack      (side = tk.LEFT, pady = 3, padx = 3)
        self.changeTreeCombo.pack (side = tk.LEFT, pady = 3, padx = 3)
        self.searchEntry.pack     (side = tk.LEFT, pady = 3, padx = 3, fill = tk.X, expand = True)
        self.searchBtn.pack       (side = tk.LEFT, pady = 3, padx = 3)
