import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import radiotest.config.config as config
import radiotest.config.configdata as configdata
import radiotest.drivers.loader as loader
import radiotest.gui.support as support


class Tab_Harm_Spur(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.test_function = None

        # Info field functions
        self.ifl = support.InfoFields()

        # Registration of validation functions
        self.v = support.Validate()
        self.int_reg = self.register(self.v.validate_int)
        self.highest_harmonic_reg = self.register(self.v.validate_highest_harmonic)
        self.pos_float_reg = self.register(self.v.validate_pos_float)

        row = 0

        # SPECTRUM ANALYZER
        self.sa_int_var = tk.IntVar(self, 0, "harmspur_rb_sel_sa_var")
        self.sa_instr_info = self.ifl.instrument_select(self,
                                                     row,
                                                     configdata.CD_FILT_SA,
                                                     "Spectrum Analyzer:",
                                                     self.sa_int_var,
                                                     self.sa_clicked_callback)


        # Equipment separator
        row += 2
        self.equipment_sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.equipment_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # *** Input fields ***

        # Ref Offset
        self.sa_ref_offset_intvar = tk.IntVar(self, config.Harm_spurs_defaults["ref_offset"],
                                              "sa_ref_offset_intvar")
        row += 1
        self.ifl.label_entry(self, row , 0, "Ref Offset:", 4, self.sa_ref_offset_intvar, self.int_reg, "dBm")

        # Display Line
        self.sa_display_line_intvar = tk.IntVar(self, config.Harm_spurs_defaults["display_line"],
                                                "sa_display_line_intvar")
        row += 1
        self.ifl.label_entry(self, row, 0, "Display Line:", 4, self.sa_display_line_intvar, self.int_reg, "dBm")

        # Fundamental Frequency
        self.sa_fundamental_doublevar = tk.DoubleVar(self, config.Harm_spurs_defaults["fundamental"],
                                               "sa_fundamental_doublevar")
        row += 1
        self.ifl.label_entry(self, row, 0, "Fundamental Frequency:", 4, self.sa_fundamental_doublevar,
                           self.pos_float_reg, "MHz")

        # Highest Harmonic
        self.sa_highest_harmonic_intvar = tk.IntVar(self, config.Harm_spurs_defaults["highest_harmonic"],
                                                    "sa_highest_harmonic_intvar")
        row += 1
        self.ifl.label_entry(self, row, 0, "Highest_Harmonic:", 4, self.sa_highest_harmonic_intvar,
                           self.highest_harmonic_reg, None)

        # Test separator
        row += 1
        self.test_sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.test_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # Test button
        row += 1
        self.test_b = tk.Button(self, text="Run Test", command=self.run_test, state=tk.DISABLED )
        self.test_b.grid(row=row, column=0)

    def register_test_function(self, test_function):
        self.test_function = test_function

    def run_test(self):
        """ This gets called when the user presses the run test button"""
        if self.test_function is None:
            return
        # Format a data structure containing the test setup to pass to the tests run function
        test_setup = dict()
        sa_dict = dict()
        sa_dict["driver_inst"] = self.sa_instr_info["driver_inst"]
        instruments = {"sa": sa_dict}
        test_setup["instruments"] = instruments
        parameters = dict()
        parameters["ref_offset"] = self.sa_ref_offset_intvar.get()
        parameters["display_line"] = self.sa_display_line_intvar.get()
        parameters["fundamental"] = self.sa_fundamental_doublevar.get()
        parameters["highest_harmonic"] = self.sa_highest_harmonic_intvar.get()
        test_setup["parameters"] = parameters
        test_setup["gui_inst"] = self
        self.test_function(test_setup)



    def sa_clicked_callback(self):
        """ Called when the spectrum analyzer radiobutton is clicked
        Calls the radiobutton handler with the required arguments"""
        self.ifl.instr_radiobutton_handler(self, self.sa_instr_info, self.test_button_enable)


    def test_button_enable(self, state):
        """ Called to enable or disable the test button"""
        ena_dis = tk.NORMAL if state is True else tk.DISABLED
        self.test_b["state"] = ena_dis


    def reset(self):
        """ Reset the tab to defaults"""
        self.ifl.reset_instrument_select(self.sa_instr_info, self.test_button_enable)

