import tkinter as tk

from tkinter import ttk
          
class TreeView(ttk.Treeview):
    def __init__(self, master, headings, columnWidths = [], *args, **kwargs):
        super().__init__(master = master, columns = headings, show = "headings", *args, **kwargs)

        self.master       = master
        self.columnWidths = columnWidths

        self.scrollBar = ttk.Scrollbar(self)

        self.configure(yscrollcommand = self.scrollBar.set)
        self.scrollBar.configure(command = self.yview)

        self.resetColumns()

        self.scrollBar.pack(side = tk.RIGHT, fill = tk.Y)

    def insertData(self, data, reversed = False):
        for i, d in enumerate(data):
            self.insert("", 0 if reversed else "end", values = d)

            if (i % 10 == 0):
                pass
                #self.master.update()
 
    def clearData(self):
        self.delete(*self.get_children())
 
    def resetColumns(self):           
        for i, col in enumerate(self["columns"]):
            self.heading(col, text = col)

            if (i < len(self.columnWidths)):
                self.column(col, minwidth = self.columnWidths[i], width = self.columnWidths[i], stretch = tk.NO)

    def getSelected(self):
        return self.item(self.focus())["values"]
