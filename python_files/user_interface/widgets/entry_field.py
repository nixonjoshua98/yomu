import tkinter as tk
import tkinter.ttk as ttk


class EntryField(ttk.Entry):
    def set_text(self, t):
        self.delete(0, tk.END)
        self.insert(0, t)
