import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import radiotest.config.config as config
import radiotest.config.configdata as configdata
import radiotest.gui.guicommon as gc
import radiotest.error_handling.exceptions as ex


class Tab_TRX_LO(gc.GuiCommon):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.av_dict = None
        self.aardvark_serial = None
        self.test_function = None
        # Registration of validation functions
        self.int_reg = self.register(self.validate_int)
        self.highest_harmonic_reg = self.register(self.validate_highest_harmonic)
        self.pos_float_reg = self.register(self.validate_pos_float)
        row = 0

        # ARBITRARY WAVEFORM GENERATOR
        self.awg_int_var = tk.IntVar(self, row, "trxlo_rb_sel_awg_var")
        self.awg_instr_info = self.instrument_select(
                                                         row,
                                                         configdata.CD_FILT_AWG,
                                                         "Arbitrary Waveform Generator:",
                                                         self.awg_int_var,
                                                         self.awg_clicked_callback,
                                                         )

        # AARDVARK CHECKBOX
        row += 2
        self.trxlo_use_aardvark_intvar = tk.IntVar(self, config.TRXLO_defaults["aardvark"],
                                                   "trxlo_use_aardvark_intvar")

        self.use_aardvark_inst = tk.Checkbutton(self, text="Use Aardvark", onvalue=1, offvalue=0,
                                                variable=self.trxlo_use_aardvark_intvar,
                                                command=self.act_on_aardvark_checkbutton,
                                                height=2, width=20)
        self.use_aardvark_inst.grid(row=row, column=0, sticky=tk.W)

        self.use_aardvark_serial = tk.Label(self, width=10, text="Serial:", anchor="w")
        self.use_aardvark_serial.grid(row=row, column=1, sticky=tk.W)

        self.use_aardvark_serial = tk.Label(self, width=20, text="N/A", anchor="w")
        self.use_aardvark_serial.grid(row=row, column=2, sticky=tk.W)



        # Equipment separator
        row += 1
        self.equipment_sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.equipment_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # TEST PARAMETERS

        # IF/Carrier Frequency
        self.awg_if_carr_freq_floatvar = tk.DoubleVar(self, config.TRXLO_defaults["if_carr_freq"],
                                                      "trxlo_if_carr_freq")
        row += 1
        self.label_entry(
                             row,
                             0,
                             "IF/Carrier Frequency:",
                             10,
                             self.awg_if_carr_freq_floatvar,
                             self.pos_float_reg,
                             "MHz")

        # Local oscillator level
        self.awg_lo_level_intvar = tk.IntVar(self,
                                             config.TRXLO_defaults["lo_level"],
                                             "trxlo_lo_level_intvar")
        row += 1
        self.label_entry(
                             row,
                             0,
                             "LO Level:",
                             4,
                             self.awg_lo_level_intvar,
                             self.int_reg,
                             "dBm")

        # Operating Frequency
        self.awg_op_freq_doublevar = tk.DoubleVar(self,
                                                  config.TRXLO_defaults["operating_freq"],
                                                  "operating_freq")
        row += 1
        self.label_entry(
                             row,
                             0,
                             "Operating Freq:",
                             10,
                             self.awg_op_freq_doublevar,
                             self.pos_float_reg,
                             "MHz")

        # USB (High LO injection)

        self.trxlo_usb_intvar = tk.IntVar(self, config.TRXLO_defaults["usb"],
                                        "trxlo_usb_intvar")
        row += 1
        self.usb_button_inst = tk.Checkbutton(self, text="USB", onvalue=1, variable=self.trxlo_usb_intvar,
                                              offvalue=0, height=2, width=4)
        self.usb_button_inst.grid(row=row, column=0, sticky=tk.W)

        # Swap LO 1 and 2 on TX

        self.trxlo_lo_swap_intvar = tk.IntVar(self, config.TRXLO_defaults["lo_swap"],
                                            "trxlo_lo_swap_intvar")
        row += 1
        self.lo_swap_button_inst = tk.Checkbutton(self, text="LO Swap on TX",
                                                  onvalue=1, offvalue=0, variable=self.trxlo_lo_swap_intvar,
                                                  height=2, width=13)
        self.lo_swap_button_inst.grid(row=row, column=0, sticky=tk.W)

        # PTT

        self.trxlo_ptt_intvar = tk.IntVar(self, config.TRXLO_defaults["ptt"],
                                        "trxlo_ptt_intvar")
        row += 1
        self.ptt_button_inst = tk.Checkbutton(self, text="PTT", onvalue=1, offvalue=0,
                                              variable=self.trxlo_ptt_intvar, height=2, width=4, state=tk.DISABLED)
        self.ptt_button_inst.grid(row=row, column=0, sticky=tk.W)

        self.aardvark_ptt_pin = tk.Label(self, width=20, text="(Aardvark pins 7,5)", anchor="w")
        self.aardvark_ptt_pin.grid(row=row, column=1, sticky=tk.W)

        # Tune

        self.trxlo_tune_intvar = tk.IntVar(self, config.TRXLO_defaults["tune"],
                                          "trxlo_tune_intvar")
        row += 1
        self.tune_button_inst = tk.Checkbutton(self, text="TUNE", onvalue=1, offvalue=0,
                                              variable=self.trxlo_tune_intvar, height=2, width=4, state=tk.DISABLED)
        self.tune_button_inst.grid(row=row, column=0, sticky=tk.W)

        self.aardvark_tune_pin = tk.Label(self, width=20, text="(Aardvark pin 8)", anchor="w")
        self.aardvark_tune_pin.grid(row=row, column=1, sticky=tk.W)


        # Test separator
        row += 1
        self.test_sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.test_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # Test button
        row += 1
        self.test_b = tk.Button(self, text="Run Test", command=self.run_test, state=tk.DISABLED)
        self.test_b.grid(row=row, column=0)

    def act_on_aardvark_checkbutton(self):
        """Called when checkbutton is checked or unchecked"""
        if self.trxlo_use_aardvark_intvar.get() == 1:
            try:
                self.av_dict = config.Loader_obj.load("AV")
                device_list = self.av_dict["instance"].get_available_devices()
                self.aardvark_serial = device_list[0]["serial"]
                self.use_aardvark_serial.configure(text=self.aardvark_serial)

            except ex.DriverError:
                self.trxlo_use_aardvark_intvar.set(0)
                self.show_error("No Aardvark device detected",
                                "Check to see the aardvark device is plugged in and not in use by another program")

                return
            state = tk.NORMAL
        else:
            self.use_aardvark_serial.configure(text="N/A")
            state = tk.DISABLED
        self.ptt_button_inst.configure(state=state)
        self.tune_button_inst.configure(state=state)

    def register_test_function(self, test_function):
        """ Register test function: Called by the test constructor"""
        self.test_function = test_function

    def run_test(self):
        """ This gets called when the user presses the run test button"""
        if self.test_function is None:
            return
        # Format a data structure containing the test setup to pass to the tests run function
        test_setup = dict()
        awg_dict = dict()
        awg_dict["driver_inst"] = self.awg_instr_info["driver_inst"]
        awg_dict["name"] = "Arbitrary Waveform Generator"
        instruments = {"awg": awg_dict}
        # Add aardvark if user specified one to use
        if self.av_dict is not None:
            instruments["av"] = self.av_dict

        test_setup["instruments"] = instruments
        parameters = dict()
        parameters["if_carr_freq"] = self.awg_if_carr_freq_floatvar.get()
        parameters["lo_level"] = self.awg_lo_level_intvar.get()
        parameters["operating_freq"] = self.awg_op_freq_doublevar.get()
        parameters["usb"] = True if self.trxlo_usb_intvar.get() == 1 else False
        parameters["lo_swap"] = True if self.trxlo_lo_swap_intvar.get() == 1 else False
        if self.aardvark_serial:
            parameters["aardvark_sn"] = self.aardvark_serial
        parameters["ptt"] = True if self.trxlo_ptt_intvar.get() == 1 else False
        parameters["tune"] = True if self.trxlo_tune_intvar.get() == 1 else False
        test_setup["parameters"] = parameters
        test_setup["gui_inst"] = self
        self.test_function(test_setup)


    def show_error(self, title=None, message=None):
        """ Display an error popup. This gets called by the test code"""
        if title is None or message is None:
            return
        tk.messagebox.showerror(title=title, message=message)
        return

    def test_button_enable(self, state):
        """ Called to enable or disable the test button"""
        ena_dis = tk.NORMAL if state is True else tk.DISABLED
        self.test_b["state"] = ena_dis

    def awg_clicked_callback(self):
        """ Called when the arbitrary waveform radiobutton is clicked
        Calls the radiobutton handler with the required arguments"""
        self.instr_radiobutton_handler(self.awg_instr_info, self.test_button_enable,
                                           self.show_error, self.awg_int_var)

    def reset(self):
        """ Reset the tab to defaults"""
        self.reset_instrument_select(self.awg_instr_info, self.test_button_enable, self.awg_int_var)
