import time as time
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import radiotest.config.config as config
import radiotest.config.configdata as configdata
import radiotest.gui.guicommon as gc


class Tab_Harm_Spur(gc.GuiCommon):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.test_function = None
        self.processed_data = None
        self.equipment_bits = 2
        # Registration of validation functions
        self.int_reg = self.register(self.validate_int)
        self.highest_harmonic_reg = self.register(self.validate_highest_harmonic)
        self.pos_float_reg = self.register(self.validate_pos_float)
        self.string_reg = self.register(self.validate_string)

        row = 0

        # SPECTRUM ANALYZER
        self.sa_int_var = tk.IntVar(self, 0, "harmspur_rb_sel_sa_var")
        self.sa_instr_info = self.instrument_select(
            row,
            configdata.CD_FILT_SA,
            "Spectrum Analyzer:",
            self.sa_int_var,
            self.sa_clicked_callback
            )

        row += 2
        self.cb_awg_intvar = tk.IntVar(self, 0, "awg_checkbox_intvar")

        self.usb_button_inst = tk.Checkbutton(self, text="Use Arbitrary Waveform Generator",
                                              command=self.act_on_awg_checkbutton, onvalue=1,
                                              variable=self.cb_awg_intvar,
                                              offvalue=0, height=2, width=30)
        self.usb_button_inst.grid(row=row, column=0, sticky=tk.W)

        row += 2

        # Optional Arbitrary Waveform Generator
        self.awg_int_var = tk.IntVar(self, 0, "harmspur_rb_sel_awg_var")
        self.awg_instr_info = self.instrument_select(
            row,
            configdata.CD_FILT_AWG,
            "Arbitrary Waveform Generator:",
            self.awg_int_var,
            self.awg_clicked_callback,
            False
        )


        # Equipment separator
        row += 2
        self.equipment_sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.equipment_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # *** Input fields ***

        # Test Project
        self.harm_project_stringvar = tk.StringVar(self, "TestProject",
                                                  "harmspur_project_stringvar")
        row += 1
        self.label_entry(row, 0, "Project Name:", 20, self.harm_project_stringvar, self.string_reg)

        # Test ID
        self.harm_id_stringvar = tk.StringVar(self, "0",
                                            "harmspur_id_stringvar")
        row += 1
        self.label_entry(row, 0, "Test ID:", 20, self.harm_id_stringvar, self.string_reg)

        # Ref Offset
        self.sa_ref_offset_intvar = tk.IntVar(self, config.Harm_spurs_defaults["ref_offset"],
                                              "harmspur_ref_offset_intvar")
        row += 1
        self.label_entry(row , 0, "Ref Offset:", 4, self.sa_ref_offset_intvar, self.int_reg, "dBm")

        # Measurement Threshold
        self.sa_display_line_intvar = tk.IntVar(self, config.Harm_spurs_defaults["display_line"],
                                                "harmspur_display_line_intvar")
        row += 1
        self.label_entry(row, 0, "Measurement Threshold:", 4, self.sa_display_line_intvar, self.int_reg, "dB")

        # Fundamental Frequency
        self.sa_fundamental_doublevar = tk.DoubleVar(self, config.Harm_spurs_defaults["fundamental"],
                                               "harmspur_fundamental_doublevar")
        row += 1
        self.label_entry(row, 0, "Fundamental Frequency:", 8, self.sa_fundamental_doublevar,
                           self.pos_float_reg, "MHz")
        row += 1

        # Highest Harmonic
        row += 1
        self.harm_highest_harmonic_intvar = tk.IntVar(self, 7, "harm_highest_harmonic_intvar")
        self.imd_radiobuttons = self.numbered_radiobuttons_create(row, "Highest Harmonic",
                                                                  self.harm_highest_harmonic_intvar, 5, 15,
                                                                  step=2,
                                                                  default=config.Harm_spurs_defaults["highest_harmonic"])

        # Arbitrary Waveform Generator Tone Level
        self.awg_tone_level_intvar = tk.IntVar(self, config.Harm_spurs_defaults["awg_tone_level"],
                                                    "harmspur_tone_level_intvar")
        row += 1
        self.tone_level_entry_item = self.label_entry(row, 0, "AWG Tone Level:", 4, self.awg_tone_level_intvar,
                         self.int_reg, unit="dBm", enabled=False)

        # Harmonics screenshot
        self.cb_harm_ss_intvar = tk.IntVar(self, 0, "harmspur_checkbox_intvar")
        row += 1
        self.harm_ss_inst = tk.Checkbutton(self, text="Capture Harmonics screenshot",
                                              onvalue=1,
                                              variable=self.cb_harm_ss_intvar,
                                              offvalue=0, height=2, width=30)
        self.harm_ss_inst.grid(row=row, column=1, sticky=tk.W)


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
        sa_dict["name"] = "Spectrum Analyzer"
        instruments = {"sa": sa_dict}
        test_setup["instruments"] = instruments
        parameters = dict()
        x = self.harm_highest_harmonic_intvar.get()
        if x is None:
            self.show_error("Entry Error", "Highest Harmonic not specified")
            return
        parameters["highest_harmonic"] = x
        parameters["use_awg"] = True if self.cb_awg_intvar.get() == 1 else False
        if parameters["use_awg"] is True:
            awg_dict = dict()
            awg_dict["driver_inst"] = self.awg_instr_info["driver_inst"]
            awg_dict["name"] = "Arbitrary Waveform Generator"
            instruments["awg"] = awg_dict
            parameters["tone_level"] = self.awg_tone_level_intvar.get()
        parameters["test_name"] = "Harmonics and Spurs"
        parameters["project_name"] = self.harm_project_stringvar.get()
        parameters["test_id"] = self.harm_id_stringvar.get()
        parameters["ref_offset"] = self.sa_ref_offset_intvar.get()
        parameters["display_line"] = self.sa_display_line_intvar.get()
        parameters["fundamental"] = self.sa_fundamental_doublevar.get()
        parameters["harm_screenshot"] = True if self.cb_harm_ss_intvar.get() == 1 else False
        test_setup["parameters"] = parameters
        test_setup["gui_inst"] = self
        processed_data = self.test_function(test_setup)
        if processed_data is None:
            return
        self.show_results(processed_data, "Harmonics Test Results")

    def act_on_awg_checkbutton(self):
        """ Enable or disable the AWG instrument select radio buttons"""
        state = True if self.cb_awg_intvar.get() == 1 else False
        self.enable_instrument_radiobuttons(self.awg_instr_info, state)
        tk_state = tk.NORMAL if state is True else tk.DISABLED
        self.tone_level_entry_item.configure(state=tk_state)
        # We must check the state of the awg radio buttons
        # and enable or disable the test button accordingly
        # If the awg is enabled, a valid awg must be selected
        # before the test button is enabled.
        if state is True:
            if self.awg_int_var.get() == 0:
                self.test_button_enable(0, 2)  # Disable the test button
            else:
                self.test_button_enable(2, 0)  # Enable the test button
        else:
            self.test_button_enable(2, 0)  # Enable the test button

    def sa_clicked_callback(self):
        """ Called when the spectrum analyzer radio buttons are  clicked
        Calls the radiobutton handler with the required arguments"""
        self.instr_radiobutton_handler(self.sa_instr_info, self.test_button_enable_sa,
                                           self.show_error, self.sa_int_var)

    def awg_clicked_callback(self):
        """ Called when the arbitrary waveform generator radio buttons are clicked
        Calls the radiobutton handler with the required arguments"""
        self.instr_radiobutton_handler(self.awg_instr_info, self.test_button_enable_awg,
                                           self.show_error, self.awg_int_var)

    def test_button_enable(self, or_bits, nand_bits):
        self.equipment_bits = self.equipment_bits | or_bits
        self.equipment_bits = self.equipment_bits & ~nand_bits
        ena_dis = tk.NORMAL if self.equipment_bits == 3 else tk.DISABLED
        self.test_b["state"] = ena_dis

    def test_button_enable_sa(self, state):
        """ Called to enable or disable the test button"""
        if state is True:
            self.test_button_enable(1, 0)
        else:
            self.test_button_enable(0, 1)


    def test_button_enable_awg(self, state):
        """ Called to enable or disable the test button"""
        if state is True:
            self.test_button_enable(2, 0)
        else:
            self.test_button_enable(0, 2)

    def reset(self):
        """ Reset the tab to defaults"""
        self.harm_id_stringvar.set(str(int(time.time())))
        self.reset_instrument_select(self.sa_instr_info, self.test_button_enable_sa, self.sa_int_var)
        self.reset_instrument_select(self.awg_instr_info, self.test_button_enable_awg, self.awg_int_var)
        self.equipment_bits = 2

