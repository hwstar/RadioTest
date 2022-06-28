import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import radiotest.config.config as config
import radiotest.config.configdata as configdata
import radiotest.drivers.loader as loader



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
        self.label_spectrum_analyzer = ttk.Label(self, width=20, anchor=tk.E, text="Spectrum Analyzer:")
        self.label_spectrum_analyzer.grid(row=0, column=0)

        self.sa_info = None


        # Get available spectrum analyzers and create radio buttons for them
        self.sa_names = ["None"]
        self.sa_names = self.sa_names + (config.Config_obj.get_instrument_names_of_type(configdata.CD_FILT_SA))
        self.rb_int_var = tk.IntVar(self, 0, "rb_sel_var")
        self.sa_radio_buttons = dict()
        self.selected_spectrum_analyzer = None
        for i, sa_name in enumerate(self.sa_names):
            self.sa_radio_buttons[sa_name] = tk.Radiobutton(self, text=sa_name, variable=self.rb_int_var, value=i,
                                                            command=self.sa_rb_sel)
            self.sa_radio_buttons[sa_name].grid(row=0, column= i + 1)
        self.pack(fill='both', expand=True)
        self.sa_obj = None

        # Format the spectrum analyzer detail fields
        self.sa_make_l = self.label_spectrum_analyzer = ttk.Label(self, width=10, anchor=tk.E, text="Make:")
        self.sa_make_l.grid(row=1, column=0)
        self.sa_make_v = self.label_spectrum_analyzer = ttk.Label(self, width=30, anchor=tk.W, text="N/A")
        self.sa_make_v.grid(row=1, column=1)

        self.sa_model_l = self.label_spectrum_analyzer = ttk.Label(self, width=10, anchor=tk.E, text="Model:")
        self.sa_model_l.grid(row=1, column=2)
        self.sa_model_v = self.label_spectrum_analyzer = ttk.Label(self, width=30, anchor=tk.W, text="N/A")
        self.sa_model_v.grid(row=1, column=3)

        self.sa_sn_l = self.label_spectrum_analyzer = ttk.Label(self, width=10, anchor=tk.E, text="Serial:")
        self.sa_sn_l.grid(row=1, column=4)
        self.sa_sn_v = self.label_spectrum_analyzer = ttk.Label(self, width=30, anchor=tk.W, text="N/A")
        self.sa_sn_v.grid(row=1, column=5)

        self.sa_fw_l = self.label_spectrum_analyzer = ttk.Label(self, width=10, anchor=tk.E, text="Firmware:")
        self.sa_fw_l.grid(row=1, column=6)
        self.sa_fw_v = self.label_spectrum_analyzer = ttk.Label(self, width=30, anchor=tk.W, text="N/A")
        self.sa_fw_v.grid(row=1, column=7)


    def sa_rb_sel(self):
        """action for spectrum analyzer radio button selection"""
        sel_sa = self.sa_names[self.rb_int_var.get()]
        if sel_sa != "None":
            try:
                self.sa_info = config.Loader_obj.load(sel_sa)
                self.selected_spectrum_analyzer = sel_sa
                drv_inst = config.Loader_obj.get_driver_instance(self.sa_info)
                self.sa_make_v.config(text=drv_inst.make)
                self.sa_model_v.config(text=drv_inst.model)
                self.sa_sn_v.config(text=drv_inst.sn)
                self.sa_fw_v.config(text=drv_inst.fw)
                self.hs_test_button_enable(True)

            except loader.LoaderError as e:
                self.hs_test_button_enable(False)
                self.sa_info = None
                self.selected_spectrum_analyzer = None
                self.sa_make_v.config(text="Offline")
                self.sa_model_v.config(text="Offline")
                self.sa_sn_v.config(text="Offline")
                self.sa_fw_v.config(text="Offline")
                tk.messagebox.showerror(title="Loader Error",
                                        message=str(e))


        else:
            self.hs_test_button_enable(False)
            self.sa_make_v.config(text="N/A")
            self.sa_model_v.config(text="N/A")
            self.sa_sn_v.config(text="N/A")
            self.sa_fw_v.config(text="N/A")

    def hs_test_button_enable(self, state):
        pass

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


