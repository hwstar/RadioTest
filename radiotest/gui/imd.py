import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import radiotest.config.config as config
import radiotest.config.configdata as configdata
import radiotest.gui.guicommon as gc




class Tab_IMD(gc.GuiCommon):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.test_function = None
        self.test_button_enable_state = 0

        # Registration of validation functions
        self.int_reg = self.register(self.validate_int)
        self.highest_harmonic_reg = self.register(self.validate_highest_harmonic)
        self.pos_float_reg = self.register(self.validate_pos_float)

        row = 0

        # SPECTRUM ANALYZER
        self.sa_int_var = tk.IntVar(self, row, "imd_rb_sel_sa_var")
        self.sa_instr_info = self.instrument_select(
                                                        row,
                                                        configdata.CD_FILT_SA,
                                                        "Spectrum Analyzer:",
                                                        self.sa_int_var,
                                                        self.sa_clicked_callback,
                                                        )

        # ARBITRARY WAVEFORM GENERATOR
        row += 2
        self.awg_int_var = tk.IntVar(self, row, "imd_rb_sel_awg_var")
        self.awg_instr_info = self.instrument_select(
                                                        row,
                                                        configdata.CD_FILT_AWG,
                                                        "Arbitrary Waveform Generator:",
                                                        self.awg_int_var,
                                                        self.awg_clicked_callback,
                                                        )

        # Equipment separator
        row += 2
        self.equipment_sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.equipment_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # TEST PARAMETERS

        # Ref Offset
        self.sa_ref_offset_intvar = tk.IntVar(self, config.IMD_defaults["ref_offset"],
                                              "sa_ref_offset_intvar")
        row += 1
        self.label_entry(row, 0, "Ref Offset:", 4, self.sa_ref_offset_intvar, self.int_reg, "dBm")

        # Tone Level

        self.awg_tone_level_intvar = tk.IntVar(self, config.IMD_defaults["tone_level"],
                                              "awg_tone_level_intvat")
        row += 1
        self.label_entry(row, 0, "Tone Level:", 4, self.awg_tone_level_intvar, self.int_reg, "dBm")


        # Display Line
        self.sa_display_line_intvar = tk.IntVar(self, config.IMD_defaults["display_line"],
                                                "sa_display_line_intvar")
        row += 1
        self.label_entry(row, 0, "Display Line:", 4, self.sa_display_line_intvar, self.int_reg, "dBm")

        # F1
        self.awg_f1_doublevar = tk.DoubleVar(self, config.IMD_defaults["f1"], "awg_f1_doublevar")
        row += 1
        self.label_entry(row, 0, "F1:", 8, self.awg_f1_doublevar,
                           self.pos_float_reg, "MHz")
        # F2
        self.awg_f2_doublevar = tk.DoubleVar(self, config.IMD_defaults["f2"], "awg_f2_doublevar")
        row += 1
        self.label_entry(row, 0, "F2:", 8, self.awg_f2_doublevar,
                           self.pos_float_reg, "MHz")

        # Span
        self.sa_span_doublevar = tk.DoubleVar(self, config.IMD_defaults["span"], "sa_span_doublevar")
        row += 1
        self.label_entry(row, 0, "Span:", 8, self.sa_span_doublevar,
                           self.pos_float_reg, "kHz")


        # Test separator
        row += 1
        self.test_sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.test_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # Test button
        row += 1
        self.test_b = tk.Button(self, text="Run Test", command=self.run_test, state=tk.DISABLED)
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
        awg_dict = dict()
        sa_dict["driver_inst"] = self.sa_instr_info["driver_inst"]
        awg_dict["driver_inst"] = self.awg_instr_info["driver_inst"]
        instruments = {"sa": sa_dict, "awg": awg_dict}
        test_setup["instruments"] = instruments
        parameters = dict()
        parameters["ref_offset"] = self.sa_ref_offset_intvar.get()
        parameters["tone_level"] = self.awg_tone_level_intvar.get()
        parameters["display_line"] = self.sa_display_line_intvar.get()
        parameters["f1"] = self.awg_f1_doublevar.get()
        parameters["f2"] = self.awg_f2_doublevar.get()
        parameters["span"] = self.sa_span_doublevar.get()
        test_setup["parameters"] = parameters
        test_setup["gui_inst"] = self
        self.test_function(test_setup)

    def show_error(self, title=None, message=None):
        """ Display an error popup. This gets called by the test code"""
        if title is None or message is None:
            return
        tk.messagebox.showerror(title=title, message=message)
        return

    def sa_clicked_callback(self):
        """ Called when the spectrum analyzer radiobutton is clicked
        Calls the radiobutton handler with the required arguments"""
        self.instr_radiobutton_handler(self.sa_instr_info, self.change_sa_selected_state,
                                           self.show_error, self.sa_int_var)


    def awg_clicked_callback(self):
        """ Called when the arbitrary waveform radiobutton is clicked
        Calls the radiobutton handler with the required arguments"""
        self.instr_radiobutton_handler(self.awg_instr_info, self.change_awg_selected_state,
                                           self.show_error, self.awg_int_var)

    def update_test_button_enable(self, or_bits, and_bits):
        """ Called to enable or disable the test button"""
        self.test_button_enable_state |= or_bits
        self.test_button_enable_state &= ~and_bits
        ena_dis = tk.NORMAL if self.test_button_enable_state  == 3 else tk.DISABLED
        self.test_b["state"] = ena_dis

    def change_sa_selected_state(self, state):
        """ Called to change the spectrum analyzer selected state"""
        or_bits = 0x1 if state is True else 0
        and_bits = 0x1 if state is False else 0

        self.update_test_button_enable(or_bits, and_bits)

    def change_awg_selected_state(self, state):
        """" Called to change the arbitrary waveform generator selected state"""
        or_bits = 0x2 if state is True else 0
        and_bits = 0x2 if state is False else 0

        self.update_test_button_enable(or_bits, and_bits)

    def reset(self):
        """ Reset the tab to defaults"""
        self.reset_instrument_select(self.sa_instr_info, self.change_sa_selected_state, self.sa_int_var)
        self.reset_instrument_select(self.awg_instr_info, self.change_awg_selected_state, self.awg_int_var)


