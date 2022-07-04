import tkinter as tk
import tkinter.ttk as ttk
import radiotest.config.config as config
import radiotest.drivers.loader as loader

#   validation of entered data
class Validate():
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

#Functions to support the entry of test parameters


class InfoFields():

    def instrument_select(self, parent, row, instr_filter, instr_text, rb_int_var, rb_sel_clicked_callback):
        """ Helper to select an instrument

        Parameters:
            parent(Frame obj): Parent frame
            row(int): Starting row to print the instrument radio buttons and instrument information (2 rows will be used)
            instr_filter(str): Instrument name string
            instr_text(int): Name of the label field used to identify the radiobutton set
            rb_int_var(IntVar obj): the Intvar object used by the radiobutton set
            rb_sel_clicked_callback(function): Function called when a radiobutton is clicked

        Returns:
             a dict containing the instrument names, radio button objects, and the make, model, serial and fw label objects
        """
        make = "N/A"
        model = "N/A"
        serial = "N/A"
        fw = "N/A"
        instr_info = dict()
        instr_info["int_var"] = rb_int_var

        # Place the instrument text label
        label_instr = ttk.Label(parent, width=20, anchor=tk.E, text=instr_text)
        label_instr.grid(row=row, column=0)

        # Get available instruments and create radio buttons for them
        instr_names = ["None"]
        instr_names = instr_names + (config.Config_obj.get_instrument_names_of_type(instr_filter))
        radio_buttons = dict()
        for i, instr_name in enumerate(instr_names):
            radio_buttons[instr_name] = tk.Radiobutton(parent, text=instr_name, variable=rb_int_var, value=i,
                                                              command=rb_sel_clicked_callback, highlightthickness=0)
            radio_buttons[instr_name].grid(row=row, column=i + 1)

        # Save the selected instrument, instrument names, and radio button objects
        instr_info["instr_selected"] = "None"
        instr_info["instr_names"] = instr_names
        instr_info["radiobuttons"] = radio_buttons

        # Create the make, model, serial number, and firmware fields
        row += 1
        make_l = ttk.Label(parent, width=10, anchor=tk.E, text="Make:")
        make_l.grid(row=row, column=0)
        instr_info["make"] = ttk.Label(parent, width=30, anchor=tk.W, text=make)
        instr_info["make"].grid(row=row, column=1)

        model_l = ttk.Label(parent, width=10, anchor=tk.E, text="Model:")
        model_l.grid(row=row, column=2)
        instr_info["model"] = ttk.Label(parent, width=30, anchor=tk.W, text=model)
        instr_info["model"].grid(row=row, column=3)

        sn_l = ttk.Label(parent, width=10, anchor=tk.E, text="Serial:")
        sn_l.grid(row=row, column=4)
        instr_info["serial"] = ttk.Label(parent, width=30, anchor=tk.W, text=serial)
        instr_info["serial"].grid(row=row, column=5)

        fw_l = ttk.Label(parent, width=10, anchor=tk.E, text="Firmware:")
        fw_l.grid(row=row, column=6)
        instr_info["fw"] = ttk.Label(parent, width=30, anchor=tk.W, text=fw)
        instr_info["fw"].grid(row=row, column=7)

        return instr_info

    def instr_radiobutton_handler(self, instr_info, test_button_enable_callback,
                                  show_error_callback, rb_int_var, busy_callback=None):
        """
        Handler for instrument radio button selection.

        Parameters:
            parent(obj) : parent frame
            instr_info (dict): A populated dictionary of state variables returned by the instrument select method
            test_button_enable_callback (function): a callback called when the test enable button is to be enabled or disabled.
            show_error_callback (function): a callback function used when a driver fails to load
            busy_callback (function) : called with an argument of True when the driver is loading, and False when loading is complete

        """
        instr_info["instr_selected"] = instr_info["instr_names"][instr_info["int_var"].get()]

        if instr_info["instr_selected"] != "None":
            try:
                if busy_callback is not None:
                    busy_callback(True)
                loader_info = config.Loader_obj.load(instr_info["instr_selected"])
                drv_inst = config.Loader_obj.get_driver_instance(loader_info)
                instr_info["driver_inst"] = drv_inst
                instr_info["make"].config(text=drv_inst.make)
                instr_info["model"].config(text=drv_inst.model)
                instr_info["serial"].config(text=drv_inst.sn)
                instr_info["fw"].config(text=drv_inst.fw)
                test_button_enable_callback(True)
                if busy_callback is not None:
                    busy_callback(False)

            except loader.LoaderError as e:
                if busy_callback is not None:
                    busy_callback(False)
                self.reset_instrument_select(instr_info, test_button_enable_callback, rb_int_var)
                show_error_callback(title="Loader Error",
                                        message=str(e))
        else:
            self.reset_instrument_select(instr_info, test_button_enable_callback, rb_int_var)

    def reset_instrument_select(self, instr_info, test_button_enable_callback, rb_int_var):
        """ Called when it is necessary to reset the selected instruments in a tab"""
        test_button_enable_callback(False) # Disable the test button
        rb_int_var.set(0) # Select the None button
        # Set the description fields to N/A
        instr_info["make"].config(text="N/A")
        instr_info["model"].config(text="N/A")
        instr_info["serial"].config(text="N/A")
        instr_info["fw"].config(text="N/A")

    def label_entry(self, parent, row, column_start, label, entry_width, entry_text_var, entry_val_reg, unit=None):
        """Helper to create a Label/Entry and optional unit Label column depending if unit is specified"""
        label_item = ttk.Label(parent, text=label)
        label_item.grid(row=row, column=column_start)
        entry_item = ttk.Entry(parent, width=entry_width, textvariable=entry_text_var,
                                           validate="key",
                                           validatecommand=(
                                               entry_val_reg, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        entry_item.grid(row=row, column=column_start+1)
        if unit is not None:
            unit_item = ttk.Label(parent, text=unit)
            unit_item.grid(row=row, column=column_start+2)



