import tkinter as tk

from tkinter import ttk

class ComboBox(ttk.Combobox):
    def __init__(self, master, values, command, widthOffset = 0, *args, **kwargs):
        super().__init__(master = master, state = "readonly", *args, **kwargs)
        
        self["values"] = values
        self.current(0)

        self.config(width = len(max(values, key = len)) + widthOffset)
        self.bind("<<ComboboxSelected>>", command)

    def getIndex(self):
        return self["values"].index(self.get())
