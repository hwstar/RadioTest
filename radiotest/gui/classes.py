import tkinter as tk
import tkinter.ttk as ttk
import radiotest.config.config as config

class Menubar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.menu_top = tk.Menu(self, tearoff=0)
        self.file_menu = tk.Menu(self.menu_top, tearoff=0)
        self.file_menu.add_command(label="Quit", command=parent.quit)
        self.menu_top.add_cascade(label="File", menu=self.file_menu)
        self.parent.parent.config(menu=self.menu_top)


class FullScreenApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        pad = 3
        self.screen_height = parent.winfo_screenheight() - pad
        self.screen_width = parent.winfo_screenwidth() - pad
        parent.geometry("{0}x{1}+0+0".format(
            self.screen_width, self.screen_height))
        self.menubar = Menubar(self)
        self.menubar.pack(side="top", fill="x")


