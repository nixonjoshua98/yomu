import tkinter as tk


class ChildWindow(tk.Toplevel):
    def __init__(self, master=None, *args, **kwargs):
        super(ChildWindow, self).__init__(master=master, *args, **kwargs)

    def show(self):
        self.grab_set()
        self.wait_window()

    def center_in_root(self, w, h):
        master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
        master_w, master_h = self.master.winfo_width(), self.master.winfo_height()

        win_w, win_h = w, h

        center_x = master_x + (master_w // 2) - (win_w // 2)
        center_y = master_y + (master_h // 2) - (win_h // 2)

        self.geometry(f"{win_w}x{win_h}+{center_x}+{center_y}")
