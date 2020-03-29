import tkinter as tk


class Toplevel(tk.Toplevel):
    def __init__(self, title: str, *, geometry: str = None, destroy_on_exit: bool = True):
        super(Toplevel, self).__init__()

        self.title(title)

        if geometry is not None:
            self.geometry(geometry)

        self.protocol("WM_DELETE_WINDOW", self.destroy if destroy_on_exit else self.withdraw)

    def center_in_root(self):
        self.master.update_idletasks()  # Updates the window sizes

        master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
        master_w, master_h = self.master.winfo_width(), self.master.winfo_height()

        self_w, self_h = self.winfo_width(), self.winfo_height()

        center_x = master_x + (master_w // 2) - (self_w // 2)
        center_y = master_y + (master_h // 2) - (self_h // 2)

        self.geometry(f"{self_w}x{self_h}+{center_x}+{center_y}")
