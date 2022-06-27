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


class Tab_Harm_Spur(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        self.pack(fill='both', expand=True)



class Tab_IMD(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        self.pack(fill='both', expand=True)


class Tabs(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=2, expand=True)
        self.harm_spur_frame = Tab_Harm_Spur(self.notebook, width=parent.screen_width, height=parent.screen_height - 60 )
        self.imd_frame = Tab_IMD(self.notebook, width=parent.screen_width, height=parent.screen_height - 60)

        self.notebook.add(self.imd_frame, text='IMD')
        self.notebook.add(self.harm_spur_frame, text='Harmonics and Spurs')

class FullScreenApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        pad = 100
        self.screen_height = parent.winfo_screenheight() - pad
        self.screen_width = parent.winfo_screenwidth() - pad
        parent.geometry("{0}x{1}+0+0".format(
            self.screen_width, self.screen_height))
        self.menubar = Menubar(self)
        self.menubar.pack(side="top", fill="x")
        self.tabs = Tabs(self)
        self.tabs.pack(side="top", fill="x")


