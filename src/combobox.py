from tkinter import ttk
from typing import Any, Sequence


class ComboBox:
    def __init__(self, master=None, command=None, values=None, current=None):

        self._data = []  # [ ["Display Value", 0], ["Text", "HiddenValue"], "Text" ]

        self._command = command

        self._combo = ttk.Combobox(master, state="readonly")

        # Add default values
        if isinstance(values, Sequence):
            self.add_options(values)

        if current is not None:
            self.set_current(current)

        self._combo.bind("<<ComboboxSelected>>", self._on_combo_change)

    def set_current(self, value):
        self._combo.current(self.values.index(value))

    def _on_combo_change(self, _):
        if self._command is not None:
            self._command(self)

    def pack(self, *args, **kwargs):
        return self._combo.pack(*args, **kwargs)

    def add_options(self, options: Sequence[Any]):
        for opt in options:
            self.add_option(opt)

    def add_option(self, option: Any):
        self._data.append(option)

        self._combo["values"] = self.display_values

        if self._combo.current() == -1:
            self._combo.current(0)

    @property
    def display_values(self) -> list:
        ls = []
        for opt in self._data:
            if isinstance(opt, Sequence):
                opt = opt[0]

            ls.append(opt)

        return ls

    @property
    def values(self) -> list:
        ls = []
        for opt in self._data:
            if isinstance(opt, Sequence):
                opt = opt[1]

            ls.append(opt)

        return ls

    @property
    def current_value(self) -> Any:
        index = self._combo.current()

        opt = self._data[index]

        if isinstance(opt, Sequence):
            opt = opt[1]

        return opt
