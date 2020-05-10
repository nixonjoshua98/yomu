import typing

from tkinter import ttk


class Combobox(ttk.Combobox):
    def __init__(self, master, values, command=None):
        super().__init__(master=master, state="readonly")

        self["values"] = values

        self.current(0)

        self._command = command
        self._prev_val = self["values"][0]

        self.bind("<<ComboboxSelected>>", self.on_selected)

    def set_command(self, com: typing.Callable):
        self._command = com

    @property
    def values(self):
        return self["values"]

    def on_selected(self, event):
        if self.get() != self._prev_val:
            self._prev_val = self.get()

            if self._command is not None:
                self._command(event)

    def get_index(self):
        return self["values"].index(self.get())
