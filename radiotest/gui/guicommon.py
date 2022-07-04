import tkinter as tk
import tkinter.ttk as ttk
import radiotest.config.config as config
import radiotest.drivers.loader as loader


class GuiCommon(ttk.Frame):

    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)


    def validate_pos_float(self, action, index, value_if_allowed,
                           prior_value, text, validation_type, trigger_type, widget_name):
        """ Validate a positive float field
        Refer to: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry-validation.html
        Parameters:
            action(int):  Action code
            index(int): Insert or delete index
            value_if_allowed(str): Edited string value to validate
            prior_value(str): String value before the edit
            text(str): The text being insered or deleted
            validation_type(str): The current value of the widget's validate option.
            trigger_type(str): the type of validation that triggered the callback
            widget_name(str): the tk name of the widget
        Returns:
            True if the entry is to be accepted, false if it is to be rejected
        """

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
        """ Validate an integer field
        Refer to: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry-validation.html
        Parameters:
            action(int):  Action code
            index(int): Insert or delete index
            value_if_allowed(str): Edited string value to validate
            prior_value(str): String value before the edit
            text(str): The text being insered or deleted
            validation_type(str): The current value of the widget's validate option.
            trigger_type(str): the type of validation that triggered the callback
            widget_name(str): the tk name of the widget
        Returns:
            True if the entry is to be accepted, false if it is to be rejected
        """
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
        """ Validate an integer field
         Refer to: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry-validation.html
        Parameters:
            action(int):  Action code
            index(int): Insert or delete index
            value_if_allowed(str): Edited string value to validate
            prior_value(str): String value before the edit
            text(str): The text being insered or deleted
            validation_type(str): The current value of the widget's validate option.
            trigger_type(str): the type of validation that triggered the callback
            widget_name(str): the tk name of the widget
        Returns:
            True if the entry is to be accepted, false if it is to be rejected

        """
        if action == "1":
            if text in "123456789":
                return True
            else:
                return False
        else:
            return True

    def instrument_select(self, row, instr_filter, instr_text, rb_int_var, rb_sel_clicked_callback):
        """ Helper to select an instrument

        Parameters:
            row(int): Starting row to print the instrument radio buttons and instrument information (2 rows will be used)
            instr_filter(str): Instrument name string
            instr_text(str): Name of the label field used to identify the radiobutton set
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
        label_instr = ttk.Label(self, width=20, anchor=tk.E, text=instr_text)
        label_instr.grid(row=row, column=0)

        # Get available instruments and create radio buttons for them
        instr_names = ["None"]
        instr_names = instr_names + (config.Config_obj.get_instrument_names_of_type(instr_filter))
        radio_buttons = dict()
        for i, instr_name in enumerate(instr_names):
            radio_buttons[instr_name] = tk.Radiobutton(self, text=instr_name, variable=rb_int_var, value=i,
                                                              command=rb_sel_clicked_callback, highlightthickness=0)
            radio_buttons[instr_name].grid(row=row, column=i + 1)

        # Save the selected instrument, instrument names, and radio button objects
        instr_info["instr_selected"] = "None"
        instr_info["instr_names"] = instr_names
        instr_info["radiobuttons"] = radio_buttons

        # Create the make, model, serial number, and firmware fields
        row += 1
        make_l = ttk.Label(self, width=10, anchor=tk.E, text="Make: ")
        make_l.grid(row=row, column=0)
        instr_info["make"] = ttk.Label(self, width=20, anchor=tk.W, text=make)
        instr_info["make"].grid(row=row, column=1)

        model_l = ttk.Label(self, width=10, anchor=tk.E, text="Model: ")
        model_l.grid(row=row, column=2)
        instr_info["model"] = ttk.Label(self, width=20, anchor=tk.W, text=model)
        instr_info["model"].grid(row=row, column=3)

        sn_l = ttk.Label(self, width=10, anchor=tk.E, text="Serial: ")
        sn_l.grid(row=row, column=4)
        instr_info["serial"] = ttk.Label(self, width=20, anchor=tk.W, text=serial)
        instr_info["serial"].grid(row=row, column=5)

        fw_l = ttk.Label(self, width=10, anchor=tk.E, text="Firmware: ")
        fw_l.grid(row=row, column=6)
        instr_info["fw"] = ttk.Label(self, width=20, anchor=tk.W, text=fw)
        instr_info["fw"].grid(row=row, column=7)

        return instr_info

    def instr_radiobutton_handler(self, instr_info, test_button_enable_callback,
                                  show_error_callback, rb_int_var, busy_callback=None):
        """
        Handler for instrument radio button selection.

        Parameters:
            instr_info (dict): A populated dictionary of state variables returned by the instrument select method
            test_button_enable_callback (function): a callback called when the test enable button is to be enabled or disabled.
            show_error_callback (function): a callback function used when a driver fails to load
            rb_int_var(IntVar): The control variable for the radio button set
            busy_callback (function) : called with an argument of True when the driver is loading, and False when loading is complete
        Returns:
            Nothing

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
        """ Called when it is necessary to reset the selected instruments in a tab
        Parameters:
            instr_info(dict):   A dictionary containing the make, model, serial number and firmware information
            test_button_enable_callback(function): A function to call to select the none radio button
            rb_int_var(IntVar): The control variable for the radio button set
        Returns:
            Nothing
        """
        test_button_enable_callback(False) # Disable the test button
        rb_int_var.set(0) # Select the None button
        # Set the description fields to N/A
        instr_info["make"].config(text="N/A")
        instr_info["model"].config(text="N/A")
        instr_info["serial"].config(text="N/A")
        instr_info["fw"].config(text="N/A")

    def label_entry(self, row, column_start, label, entry_width, entry_text_var, entry_val_reg, unit=None):
        """Helper to create a Label/Entry and optional unit Label column depending if unit is specified
        Parameters:
            row(int): The row number for the label entry
            column_start(int): The column number entry where the label entry will start (uses 2 or 3 columns)
            entry_width(int): Entry width in characters
            entry_text_var(StrVar): Control variable for the entry
            entry_val_reg: Validation registration object
            unit(str): (optional) A string containing the unit name
        Returns:
              Nothing
        """
        label_item = ttk.Label(self, text=label)
        label_item.grid(row=row, column=column_start)
        entry_item = ttk.Entry(self, width=entry_width, textvariable=entry_text_var,
                                           validate="key",
                                           validatecommand=(
                                               entry_val_reg, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        entry_item.grid(row=row, column=column_start+1)
        if unit is not None:
            unit_item = ttk.Label(self, text=unit)
            unit_item.grid(row=row, column=column_start+2)

    def format_float_as_string(self, value, precision):
        """ Format a floating point number as a string with the supplied precision
        Parameters:
            value(float):   The value to convert to a string
            precision(int): The number of digits to the right of the decimal point to include
        Returns:
            A string representing the number
        """
        f_string = "{value:." + str(precision) + "f}"
        return f_string.format(value)
