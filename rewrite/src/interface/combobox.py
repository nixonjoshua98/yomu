from tkinter import ttk


class Combobox(ttk.Combobox):
	def __init__(self, master, values, command=None):
		super(Combobox, self).__init__(master=master, state="readonly")

		self["values"] = values

		self.current(0)

		self._command = command
		self._prev_val = None

		self.bind("<<ComboboxSelected>>", self.on_selected)

	def config(self, *args, **kwargs):
		self._command = kwargs.pop("command", None)

		super().config(*args, **kwargs)

	@property
	def val_index(self):
		return self["values"].index(self.get())

	def on_selected(self, event=None):
		# Only call the callback if the value has changed
		if self.get() != self._prev_val:
			self._prev_val = self.get()

			if self._command is not None:
				self.after(10, self._command, event)  # Added a very short delay
