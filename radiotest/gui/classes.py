import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import re
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

        # Registration of validation functions
        self.int_reg = self.register(self.validate_int)
        self.highest_harmonic_reg = self.register(self.validate_highest_harmonic)
        self.pos_float_reg = self.register(self.validate_pos_float)


        # SPECTRUM ANALYZER
        self.label_spectrum_analyzer = ttk.Label(self, width=20, anchor=tk.E, text="Spectrum Analyzer:")
        self.label_spectrum_analyzer.grid(row=0, column=0)


        self.sa_info = None

        # Get available spectrum analyzers and create radio buttons for them
        self.sa_names = ["None"]
        self.sa_names = self.sa_names + (config.Config_obj.get_instrument_names_of_type(configdata.CD_FILT_SA))
        self.sa_rb_int_var = tk.IntVar(self, 0, "rb_sel_sa_var")
        self.sa_radio_buttons = dict()
        self.selected_spectrum_analyzer = None
        for i, sa_name in enumerate(self.sa_names):
            self.sa_radio_buttons[sa_name] = tk.Radiobutton(self, text=sa_name, variable=self.sa_rb_int_var, value=i,
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

        # *** Input fields ***

        # Ref Offset
        self.sa_ref_offset_l = ttk.Label(self, text="Ref Offset:")
        self.sa_ref_offset_l.grid(row=2, column=0)
        self.sa_ref_offset_intvar = tk.IntVar(self, config.Harm_spurs_defaults["ref_offset"],
                                              "sa_ref_offset_intvar")
        self.sa_ref_offset_e = ttk.Entry(self, width=4, textvariable=self.sa_ref_offset_intvar,
                                         validate="key",
                                         validatecommand=(self.int_reg, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.sa_ref_offset_e.grid(row=2, column=1)
        self.sa_ref_offset_dbm_l = ttk.Label(self, text="dBm")
        self.sa_ref_offset_dbm_l.grid(row=2, column=2)

        # Display Line

        self.sa_display_line_l = ttk.Label(self, text="Display Line:")
        self.sa_display_line_l.grid(row=3, column=0)
        self.sa_display_line_intvar = tk.IntVar(self, config.Harm_spurs_defaults["display_line"],
                                                "sa_display_line_intvar")
        self.sa_display_line_e = ttk.Entry(self, width=4, textvariable=self.sa_display_line_intvar,
                                        validate="key",
                                        validatecommand=(self.int_reg, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.sa_display_line_e.grid(row=3, column=1)
        self.sa_display_line_dbm_l = ttk.Label(self, text="dBm")
        self.sa_display_line_dbm_l.grid(row=3, column=2)

        # Fundamental Frequency

        self.sa_fundamental_l = ttk.Label(self, text="Fundamental Frequency:")
        self.sa_fundamental_l.grid(row=4, column=0)
        self.sa_fundamental_intvar = tk.IntVar(self, config.Harm_spurs_defaults["fundamental"],
                                                "sa_fundamental_intvar")
        self.sa_fundamental_e = ttk.Entry(self, width=8, textvariable=self.sa_fundamental_intvar,
                                        validate="key",
                                        validatecommand=(self.pos_float_reg,
                                                         '%d', '%i', '%P', '%s', '%S', '%v', '%V','%W'))
        self.sa_fundamental_e.grid(row=4, column=1)
        self.sa_fundamental_dbm_l = ttk.Label(self, text="MHz")
        self.sa_fundamental_dbm_l.grid(row=4, column=2)

        # Highest Harmonic

        self.sa_highest_harmonic_l = ttk.Label(self, text="Highest Harmonic:")
        self.sa_highest_harmonic_l.grid(row=5, column=0)
        self.sa_highest_harmonic_intvar = tk.IntVar(self, config.Harm_spurs_defaults["highest_harmonic"],
                                                "sa_highest_harmonic_intvar")
        self.sa_highest_harmonic_e = ttk.Entry(self, width=2, textvariable=self.sa_highest_harmonic_intvar,
                                        validate="key",
                                        validatecommand=(self.highest_harmonic_reg,
                                                         '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.sa_highest_harmonic_e.grid(row=5, column=1)




    def sa_rb_sel(self):
        """action for radio button selection"""
        sel_sa = self.sa_names[self.sa_rb_int_var.get()]
        if sel_sa != "None":
            try:
                self.sa_info = config.Loader_obj.load(sel_sa)
                self.selected_spectrum_analyzer = sel_sa
                drv_inst = config.Loader_obj.get_driver_instance(self.sa_info)
                self.sa_make_v.config(text=drv_inst.make)
                self.sa_model_v.config(text=drv_inst.model)
                self.sa_sn_v.config(text=drv_inst.sn)
                self.sa_fw_v.config(text=drv_inst.fw)
                self.test_button_enable(True)

            except loader.LoaderError as e:
                self.test_button_enable(False)
                self.sa_info = None
                self.selected_spectrum_analyzer = None
                self.sa_make_v.config(text="Offline")
                self.sa_model_v.config(text="Offline")
                self.sa_sn_v.config(text="Offline")
                self.sa_fw_v.config(text="Offline")
                tk.messagebox.showerror(title="Loader Error",
                                        message=str(e))


        else:
            self.test_button_enable(False)
            self.sa_make_v.config(text="N/A")
            self.sa_model_v.config(text="N/A")
            self.sa_sn_v.config(text="N/A")
            self.sa_fw_v.config(text="N/A")

    def reset(self):
        """ Reset the tab to defaults"""
        self.test_button_enable(False) # Disables the test button
        self.sa_rb_int_var.set(0) # Sets the SA to none
        self.sa_info = None
        self.selected_spectrum_analyzer = None
        self.test_button_enable(False)
        self.sa_make_v.config(text="N/A")
        self.sa_model_v.config(text="N/A")
        self.sa_sn_v.config(text="N/A")
        self.sa_fw_v.config(text="N/A")

    def test_button_enable(self, state):
        pass


    def validate_pos_float(self, action, index, value_if_allowed,
                           prior_value, text, validation_type, trigger_type, widget_name):
        """ Validate a positive float field"""
        if (action == '1'):
            if text in '0123456789.':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True


    def validate_int(self, action, index, value_if_allowed,
                     prior_value, text, validation_type, trigger_type, widget_name):
        """ Validate an integer field"""
        if action == "1":
            if text in "0123456789-":
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    if value_if_allowed == "-":
                        return True
                    return False
            else:
                return False
        else:
            return True

    def validate_highest_harmonic(self, action, index, value_if_allowed,
                                  prior_value, text, validation_type, trigger_type, widget_name):
        """ Validate an integer field"""
        if action == "1":
            if text in "123456789":
                return True
            else:
                return False
        else:
            return True




class Tab_IMD(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        self.test_button_mask = 0
        self.test_button_enable(0, 3)

        # SPECTRUM ANALYZER
        self.label_spectrum_analyzer = ttk.Label(self, width=20, anchor=tk.E, text="Spectrum Analyzer:")
        self.label_spectrum_analyzer.grid(row=0, column=0)

        self.sa_info = None

        # Get available spectrum analyzers and create radio buttons for them
        self.sa_names = ["None"]
        self.sa_names = self.sa_names + (config.Config_obj.get_instrument_names_of_type(configdata.CD_FILT_SA))
        self.sa_rb_int_var = tk.IntVar(self, 0, "rb_sel_sa_var")
        self.sa_radio_buttons = dict()
        self.selected_spectrum_analyzer = None
        for i, sa_name in enumerate(self.sa_names):
            self.sa_radio_buttons[sa_name] = tk.Radiobutton(self, text=sa_name, variable=self.sa_rb_int_var, value=i,
                                                            command=self.sa_rb_sel)
            self.sa_radio_buttons[sa_name].grid(row=0, column=i + 1)
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


        # ARBITRARY WAVEFORM GENERATOR
        self.label_arb_waveform_generator = ttk.Label(self, width=20, anchor=tk.E, text="Arb Waveform Gen:")
        self.label_arb_waveform_generator.grid(row=8, column=0)
        self.arb_info = None

        # Get available arbitrary waveform generators and create radio buttons for them
        self.arb_names = ["None"]
        self.arb_names = self.arb_names + (config.Config_obj.get_instrument_names_of_type(configdata.CD_FILT_AWG))
        self.arb_rb_int_var = tk.IntVar(self, 0, "rb_sel_arb_var")
        self.arb_radio_buttons = dict()
        self.selected_arb_waveform_generator = None
        for i, arb_name in enumerate(self.arb_names):
            self.sa_radio_buttons[arb_name] = tk.Radiobutton(self, text=arb_name, variable=self.arb_rb_int_var, value=i,
                                                            command=self.arb_rb_sel)
            self.sa_radio_buttons[arb_name].grid(row=8, column=i + 1)
        self.pack(fill='both', expand=True)
        self.arb_obj = None

        # Format the arb waveform generator detail fields
        self.arb_make_l = self.label_arb_waveform_generator = ttk.Label(self, width=10, anchor=tk.E, text="Make:")
        self.arb_make_l.grid(row=10, column=0)
        self.arb_make_v = self.label_arb_waveform_generator = ttk.Label(self, width=30, anchor=tk.W, text="N/A")
        self.arb_make_v.grid(row=10, column=1)

        self.arb_model_l = self.label__arb_waveform_generator = ttk.Label(self, width=10, anchor=tk.E, text="Model:")
        self.arb_model_l.grid(row=10, column=2)
        self.arb_model_v = self.label__arb_waveform_generator = ttk.Label(self, width=30, anchor=tk.W, text="N/A")
        self.arb_model_v.grid(row=10, column=3)

        self.arb_sn_l = self.label_arb_waveform_generator = ttk.Label(self, width=10, anchor=tk.E, text="Serial:")
        self.arb_sn_l.grid(row=10, column=4)
        self.arb_sn_v = self.label_arb_waveform_generator = ttk.Label(self, width=30, anchor=tk.W, text="N/A")
        self.arb_sn_v.grid(row=10, column=5)

        self.arb_fw_l = self.label_arb_waveform_generator = ttk.Label(self, width=10, anchor=tk.E, text="Firmware:")
        self.arb_fw_l.grid(row=10, column=6)
        self.arb_fw_v = self.label__arb_waveform_generator = ttk.Label(self, width=30, anchor=tk.W, text="N/A")
        self.arb_fw_v.grid(row=10, column=7)

    def sa_rb_sel(self):
        """action for radio button selection"""
        sel_sa = self.sa_names[self.sa_rb_int_var.get()]
        if sel_sa != "None":
            try:
                self.sa_info = config.Loader_obj.load(sel_sa)
                self.selected_spectrum_analyzer = sel_sa
                drv_inst = config.Loader_obj.get_driver_instance(self.sa_info)
                self.sa_make_v.config(text=drv_inst.make)
                self.sa_model_v.config(text=drv_inst.model)
                self.sa_sn_v.config(text=drv_inst.sn)
                self.sa_fw_v.config(text=drv_inst.fw)
                self.test_button_enable(1, 0)

            except loader.LoaderError as e:
                self.test_button_enable(0, 1)
                self.sa_info = None
                self.selected_spectrum_analyzer = None
                self.sa_make_v.config(text="Offline")
                self.sa_model_v.config(text="Offline")
                self.sa_sn_v.config(text="Offline")
                self.sa_fw_v.config(text="Offline")
                tk.messagebox.showerror(title="Loader Error",
                                        message=str(e))


        else:
            self.test_button_enable(0,1)
            self.sa_make_v.config(text="N/A")
            self.sa_model_v.config(text="N/A")
            self.sa_sn_v.config(text="N/A")
            self.sa_fw_v.config(text="N/A")

    def arb_rb_sel(self):
        """action for radio button selection"""
        sel_arb = self.arb_names[self.arb_rb_int_var.get()]
        if sel_arb != "None":
            try:
                self.arb_info = config.Loader_obj.load(sel_arb)
                self.selected_arb_waveform_generator = sel_arb
                drv_inst = config.Loader_obj.get_driver_instance(self.arb_info)
                self.arb_make_v.config(text=drv_inst.make)
                self.arb_model_v.config(text=drv_inst.model)
                self.arb_sn_v.config(text=drv_inst.sn)
                self.arb_fw_v.config(text=drv_inst.fw)
                self.test_button_enable(2, 0)

            except loader.LoaderError as e:
                self.test_button_enable(0, 2)
                self.arb_info = None
                self.selected_arb_waveform_generator = None
                self.arb_make_v.config(text="Offline")
                self.arb_model_v.config(text="Offline")
                self.arb_sn_v.config(text="Offline")
                self.arb_fw_v.config(text="Offline")
                tk.messagebox.showerror(title="Loader Error",
                                        message=str(e))


        else:
            self.test_button_enable(0, 2)
            self.arb_make_v.config(text="N/A")
            self.arb_model_v.config(text="N/A")
            self.arb_sn_v.config(text="N/A")
            self.arb_fw_v.config(text="N/A")


    def reset(self):
        """ Reset the tab to defaults"""
        self.test_button_mask = 0  # Disables the test button

        self.sa_rb_int_var.set(0)  # Sets the SA to none
        self.sa_info = None
        self.selected_spectrum_analyzer = None
        self.sa_make_v.config(text="N/A")
        self.sa_model_v.config(text="N/A")
        self.sa_sn_v.config(text="N/A")
        self.sa_fw_v.config(text="N/A")

        self.arb_rb_int_var.set(0)  # Sets the ARB to none
        self.arb_info = None
        self.selected_arb_waveform_generator = None
        self.arb_make_v.config(text="N/A")
        self.arb_model_v.config(text="N/A")
        self.arb_sn_v.config(text="N/A")
        self.arb_fw_v.config(text="N/A")


    def test_button_enable(self, or_bits, mask_bits):
        self.test_button_mask = self.test_button_mask | or_bits
        self.test_button_mask = self.test_button_mask & ~mask_bits
        # Check mask bits and enable or disable the test button
        if self.test_button_mask == 3:
            pass
        else:
            pass



class Tabs(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=2, expand=True)


        self.tab_frames = {}
        harm_spur_frame = Tab_Harm_Spur(self.notebook, width=parent.screen_width, height=parent.screen_height - 60 )
        self.tab_frames["harmspur"] = harm_spur_frame
        imd_frame = Tab_IMD(self.notebook, width=parent.screen_width, height=parent.screen_height - 60)
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


