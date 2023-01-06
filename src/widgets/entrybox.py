import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class EntryBox(ttk.Entry):
    def __init__(self, *args, text=None, type_: str = "text", **kwargs):
        super(EntryBox, self).__init__(*args, **kwargs)

        self._configure_validation(type_)

        if text is not None:
            self.insert(0, text)

    def set_text(self, text):
        self.delete(0, tk.END)
        self.insert(0, text)

    @staticmethod
    def get_input_validator(type_: str) -> Optional[Callable[[str], bool]]:
        return {
            "float": _float_validator
        }.get(type_)

    def _configure_validation(self, type_: str):
        validator = self.get_input_validator(type_)

        if validator is not None:
            registered_validator = self.master.register(validator)

            self.configure(validate="key", validatecommand=(registered_validator, "%P"))


def _float_validator(val: str) -> bool:
    if str(val) == "":
        return True

    try:
        float(val)
    except ValueError:
        return False

    return True
