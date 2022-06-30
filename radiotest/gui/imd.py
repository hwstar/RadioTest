import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import radiotest.config.config as config
import radiotest.config.configdata as configdata
import radiotest.drivers.loader as loader
import radiotest.gui.support as support




class Tab_IMD(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

        self.test_button_enable_state = 0

        # Info field functions
        self.ifl = support.InfoFields()

        # Registration of validation functions
        self.v = support.Validate()
        self.int_reg = self.register(self.v.validate_int)
        self.highest_harmonic_reg = self.register(self.v.validate_highest_harmonic)
        self.pos_float_reg = self.register(self.v.validate_pos_float)

        row = 0

        # SPECTRUM ANALYZER
        self.sa_int_var = tk.IntVar(self, row, "imd_rb_sel_sa_var")
        self.sa_instr_info = self.ifl.instrument_select(self,
                                                        row,
                                                        configdata.CD_FILT_SA,
                                                        "Spectrum Analyzer:",
                                                        self.sa_int_var,
                                                        self.sa_clicked_callback)

        # ARBITRARY WAVEFORM GENERATOR
        row += 2
        self.awg_int_var = tk.IntVar(self, row, "imd_rb_sel_awg_var")
        self.awg_instr_info = self.ifl.instrument_select(self,
                                                        row,
                                                        configdata.CD_FILT_AWG,
                                                        "Arbitrary Waveform Generator:",
                                                        self.awg_int_var,
                                                        self.awg_clicked_callback)

        # Equipment separator
        row += 2
        self.equipment_sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.equipment_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # TEST PARAMETERS

        # Ref Offset
        self.sa_ref_offset_intvar = tk.IntVar(self, config.IMD_defaults["ref_offset"],
                                              "sa_ref_offset_intvar")
        row += 1
        self.ifl.label_entry(self, row, 0, "Ref Offset:", 4, self.sa_ref_offset_intvar, self.int_reg, "dBm")

        # Tone Level

        self.awg_tone_level_intvar = tk.IntVar(self, config.IMD_defaults["tone_level"],
                                              "awg_tone_level_intvat")
        row += 1
        self.ifl.label_entry(self, row, 0, "Tone Level:", 4, self.awg_tone_level_intvar, self.int_reg, "dBm")


        # Display Line
        self.sa_display_line_intvar = tk.IntVar(self, config.IMD_defaults["display_line"],
                                                "sa_display_line_intvar")
        row += 1
        self.ifl.label_entry(self, row, 0, "Display Line:", 4, self.sa_display_line_intvar, self.int_reg, "dBm")

        # F1
        self.awg_f1_doublevar = tk.DoubleVar(self, config.IMD_defaults["f1"], "awg_f1_doublevar")
        row += 1
        self.ifl.label_entry(self, row, 0, "F1:", 8, self.awg_f1_doublevar,
                           self.pos_float_reg, "MHz")
        # F2
        self.awg_f2_doublevar = tk.DoubleVar(self, config.IMD_defaults["f2"], "awg_f2_doublevar")
        row += 1
        self.ifl.label_entry(self, row, 0, "F2:", 8, self.awg_f2_doublevar,
                           self.pos_float_reg, "MHz")

        # Span
        self.sa_span_doublevar = tk.DoubleVar(self, config.IMD_defaults["span"], "sa_span_doublevar")
        row += 1
        self.ifl.label_entry(self, row, 0, "Span:", 8, self.sa_span_doublevar,
                           self.pos_float_reg, "kHz")

    def sa_clicked_callback(self):
        """ Called when the spectrum analyzer radiobutton is clicked
        Calls the radiobutton handler with the required arguments"""
        self.ifl.instr_radiobutton_handler(self, self.sa_instr_info, self.change_sa_selected_state)


    def awg_clicked_callback(self):
        """ Called when the arbitrary waveform radiobutton is clicked
        Calls the radiobutton handler with the required arguments"""
        self.ifl.instr_radiobutton_handler(self, self.awg_instr_info, self.change_awg_selected_state)

    def update_test_button_enable(self, or_bits, and_bits):
        """ Called to enable or disable the test button"""
        self.test_button_enable_state |= or_bits
        self.test_button_enable_state &= and_bits
        if self.test_button_enable_state == 3:
            pass  # TODO: Enable test button here
        else:
            pass  # TODO: Disable test button here


    def change_sa_selected_state(self, state):
        """ Called to change the spectrum analyzer selected state"""
        or_bits = 0x1 if state is True else 0
        and_bits = ~0x1 if state is False else 0

        self.update_test_button_enable(or_bits, and_bits)

    def change_awg_selected_state(self, state):
        """" Called to change the arbitrary waveform generator selected state"""
        or_bits = 0x2 if state is True else 0
        and_bits = ~0x2 if state is False else 0

        self.update_test_button_enable(or_bits, and_bits)

    def reset(self):
        """ Reset the tab to defaults"""
        self.ifl.reset_instrument_select(self.sa_instr_info, self.change_sa_selected_state)
        self.ifl.reset_instrument_select(self.awg_instr_info, self.change_awg_selected_state)


