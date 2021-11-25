import tkinter as tk
from tkinter import ttk


class EntryBox(ttk.Entry):
    def __init__(self, *args, text=None, numbers_only: bool = False, **kwargs):
        super(EntryBox, self).__init__(*args, **kwargs)

        if numbers_only:
            validation = self.master.register(self._validate_numbers_only)

            self.configure(validate="key", validatecommand=(validation, "%P"))

        if text is not None:
            self.insert(0, text)

    def set_text(self, text):
        self.delete(0, tk.END)
        self.insert(0, text)

    @staticmethod
    def _validate_numbers_only(val) -> bool:
        if str(val) == "":
            return True

        try:
            float(val)
        except ValueError:
            return False

        return True
