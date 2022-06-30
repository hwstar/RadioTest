import tkinter as tk
import tkinter.ttk as ttk
import radiotest.gui.harmspur as harmspur
import radiotest.gui.imd as imd



class Menubar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.menu_top = tk.Menu(self, tearoff=0)
        self.file_menu = tk.Menu(self.menu_top, tearoff=0)
        self.file_menu.add_command(label="Quit", command=parent.quit)
        self.menu_top.add_cascade(label="File", menu=self.file_menu)
        self.parent.parent.config(menu=self.menu_top)


class Tabs(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=2, expand=True)

        self.tab_frames = {}
        harm_spur_frame = harmspur.Tab_Harm_Spur(self.notebook, width=parent.screen_width, height=parent.screen_height - 60 )
        self.tab_frames["harmspur"] = harm_spur_frame
        imd_frame = imd.Tab_IMD(self.notebook, width=parent.screen_width, height=parent.screen_height - 60)
        self.tab_frames["imd"] = imd_frame

        self.notebook.add(imd_frame, text='IMD')
        self.notebook.add(harm_spur_frame, text='Harmonics and Spurs')
        self.notebook.bind("<<NotebookTabChanged>>", self.notebook_tab_changed)


    def notebook_tab_changed(self, *args):
        """This is called when a user changes the active tab"""
        for tab in self.tab_frames.values():
            tab.reset()  # Call the reset function for all the tabs




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


