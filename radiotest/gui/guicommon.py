import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showerror
import radiotest.config.config as config
import radiotest.drivers.loader as loader
import io

class GuiCommon(ttk.Frame):

    def __init__(self, parent, **kwargs):
        self.image_top = None
        self.image_top_label = None
        self.python_photo_image = None


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
            text(str): The text being inserted or deleted
            validation_type(str): The current value of the widget's validate option.
            trigger_type(str): the type of validation that triggered the callback
            widget_name(str): the tk name of the widget
        Returns:
            True if the entry is to be accepted, false if it is to be rejected
        """

        if  action == '1':
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
            text(str): The text being inserted or deleted
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
            text(str): The text being inserted or deleted
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

    def validate_string(self, action, index, value_if_allowed,
                        prior_value, text, validation_type, trigger_type, widget_name):
        """ Validate an integer field
                Refer to: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry-validation.html
               Parameters:
                   action(int):  Action code
                   index(int): Insert or delete index
                   value_if_allowed(str): Edited string value to validate
                   prior_value(str): String value before the edit
                   text(str): The text being inserted or deleted
                   validation_type(str): The current value of the widget's validate option.
                   trigger_type(str): the type of validation that triggered the callback
                   widget_name(str): the tk name of the widget
               Returns:
                   True if the entry is to be accepted, false if it is to be rejected
        """
        return True

    def instrument_select(self, row, instr_filter, instr_text, rb_int_var, rb_sel_clicked_callback, enabled=True):
        """ Helper to select an instrument

        Parameters:
            row(int): Starting row to print the instrument radio buttons and instrument information (2 rows will be used)
            instr_filter(str): Instrument name string
            instr_text(str): Name of the label field used to identify the radiobutton set
            rb_int_var(IntVar obj): the Intvar object used by the radiobutton set
            rb_sel_clicked_callback(function): Function called when a radiobutton is clicked
            enabled(bool): Enable or disable the radio buttons

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
        state = tk.NORMAL if enabled is True else tk.DISABLED

        for i, instr_name in enumerate(instr_names):
            radio_buttons[instr_name] = tk.Radiobutton(self, text=instr_name, variable=rb_int_var, value=i,
                                                       command=rb_sel_clicked_callback,
                                                       highlightthickness=0, state=state)
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

    def enable_instrument_radiobuttons(self, instr_info, enabled=True):
        """"
        Enable or disable the radio buttons for an instrument

        Parameters:
                instr_info(obj):    Information for the instrument
                enabled(bool):  Enable or disable the buttons for the instrument
        Returns:
                Nothing

        """
        state = tk.NORMAL if enabled is True else tk.DISABLED
        for radiobutton in instr_info["radiobuttons"].values():
            radiobutton.configure(state=state)



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

    def label_entry(self, row, column_start, label, entry_width, entry_text_var, entry_val_reg, unit=None,
                    enabled = True):
        """Helper to create a Label/Entry and optional unit Label column depending if unit is specified
        Parameters:
            row(int): The row number for the label entry
            column_start(int): The column number entry where the label entry will start (uses 2 or 3 columns)
            entry_width(int): Entry width in characters
            entry_text_var(StrVar): Control variable for the entry
            entry_val_reg(obj): Validation registration object
            unit(str): (optional) A string containing the unit name
            enabled(bool): Enable the entry if true
        Returns:
              entry_item
        """
        label_item = ttk.Label(self, text=label)
        label_item.grid(row=row, column=column_start)
        entry_item = ttk.Entry(self, width=entry_width, textvariable=entry_text_var,
                                           validate="key",
                                           validatecommand=(
                                               entry_val_reg, '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
        entry_item.grid(row=row, column=column_start+1)
        state = tk.NORMAL if enabled is True else tk.DISABLED
        entry_item.configure(state = state)
        if unit is not None:
            unit_item = ttk.Label(self, text=unit)
            unit_item.grid(row=row, column=column_start+2)
        return entry_item


    def show_error(self, title=None, message=None):
        """ Display an error popup. This gets called by the test code
        Parameters:
            title(str): A title string for the error message popup
            message(str): The error message to display
        Returns:
            Nothing
        """

        if title is None or message is None:
            return
        tk.messagebox.showerror(title=title, message=message)
        return

    def show_results(self, processed_data, title="Test Results"):
        """ Show the results of a test
        Parameters:
            processed_data(obj)
        Returns:
            Nothing
        """

        def show_results_test_metrics(row_in):
            """
            This internal function handles displaying the test parameters
            It is passed the starting row, and it returns the next row which can be used
            """
            metrics = processed_data["test_metrics"]
            # Format test parameters
            heading = tk.Label(self.results_top, width=30,
                               text="Test Metrics", font="bold", anchor="w")
            heading.grid(row=row_in, column=0)

            row_in += 1
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Metric", font="TkHeadingFont").grid(row=row_in, column=0, sticky=tk.NSEW)
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Value", font="TkHeadingFont").grid(row=row_in, column=1, sticky=tk.NSEW)
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Unit", font="TkHeadingFont").grid(row=row_in, column=2, sticky=tk.NSEW)

            row_in += 1
            for metric in metrics:
                keys = list(metric.keys())
                values = list(metric.values())

                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=keys[0]).grid(row=row_in, column=0, sticky=tk.NSEW)
                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=values[0]).grid(row=row_in, column=1, sticky=tk.NSEW)
                unit = metric["Unit"] if "Unit" in keys else "-"
                tk.Label(self.results_top, relief=tk.GROOVE, width=30, text=unit).grid(row=row_in, column=2,
                                                                                       sticky=tk.NSEW)

                row_in += 1
            return row_in

        def show_results_test_parameters(row_in):
            """
            This internal function handles displaying the test parameters
            It is passed the starting row, and it returns the next row which can be used
            """
            parameters = processed_data["test_parameters"]

            # Format test parameters
            heading = tk.Label(self.results_top, width=30,
                               text="Test Parameters", font="bold", anchor="w")
            heading.grid(row=row_in, column=0)

            row_in += 1
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Parameter", font="TkHeadingFont").grid(row=row_in, column=0, sticky=tk.NSEW)
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Value", font="TkHeadingFont").grid(row=row_in, column=1, sticky=tk.NSEW)
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Unit", font="TkHeadingFont").grid(row=row_in, column=2, sticky=tk.NSEW)

            row_in += 1
            for parameter in parameters:
                keys = list(parameter.keys())
                values = list(parameter.values())

                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=keys[0]).grid(row=row_in, sticky=tk.NSEW)
                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=values[0]).grid(row=row_in, column=1, sticky=tk.NSEW)

                unit = parameter["Unit"] if "Unit" in keys else "-"
                tk.Label(self.results_top, relief=tk.GROOVE, width=30, text=unit).grid(row=row_in, column=2,
                                                                                       sticky=tk.NSEW)
                row_in += 1
            return row_in

        def show_results_info(row_in, results_set):
            """
            This internal function handles displaying the test parameters
            It is passed the starting row, and it returns the next row which can be used
            """



            results_header = list(results_set.keys())[0]

            # Get the keys for the first row
            # These will determine the number of colunms we will require
            first_row = results_set[results_header][0]
            keys_first_row = list(first_row.keys())
            # The number of columns will equal the number of keys
            columns = len(keys_first_row)

            # Format test parameter heading
            heading = tk.Label(self.results_top, width=30,
                               text=results_header, font="bold", anchor="w")
            heading.grid(row=row_in, column=0,sticky=tk.NSEW)

            row_in += 1

            # Format the table header
            for column in range(0, columns):
                table_header = tk.Label(self.results_top, width=30,
                                        text=keys_first_row[column], font="TkHeadingFont",
                                        relief=tk.GROOVE, justify=tk.LEFT)
                table_header.grid(row=row_in, column=column, sticky=tk.NSEW)

            row_in += 1

            # Format the data
            for row_info in results_set[results_header]:
                row_info_values = list(row_info.values())
                for column in range(0, columns):
                    table_header = tk.Label(self.results_top, width=30,
                                            text=row_info_values[column],
                                            relief=tk.GROOVE, justify=tk.LEFT)
                    table_header.grid(row=row_in, column=column, sticky=tk.NSEW)
                row_in += 1

            return row_in

        self.results_top = tk.Toplevel(config.Root_obj)
        self.results_top.title(title)

        row = 0

        # Show test metrics

        row = show_results_test_metrics(row)

        # Show test parameters

        row = show_results_test_parameters(row)

        # Show result sets

        for result in processed_data["results"]:
            row = show_results_info(row, result)

        # Present window

        self.results_top.transient(config.Root_obj)




    def show_image(self, image_info, test_name="sometest", directory="/tmp", project_name="None", test_id="12345678"):
        """ Pops up a transient window and displays an in-memory BMP file
        Parameters:
            image_info(obj): In-memory image to display
            test_name(str): Name of the test which identifies what was tested
            directory(str): Path where test results are stored
            project_name(str): A string identifying a project
            test_id(str): A unique identifier for the test
        Returns:
            Nothing

        """
        def pressed():
            save_path = directory+"/"+project_name+"/"+test_id+"/"+test_name+".bmp"
            pass


        pil_image = Image.open(io.BytesIO(image_info["data"]))
        self.image_top = tk.Toplevel(config.Root_obj)
        self.image_top.title(image_info["name"])
        self.python_photo_image = ImageTk.PhotoImage(pil_image)
        self.image_top_label = tk.Label(self.image_top, image=self.python_photo_image)
        self.image_top_label.grid(columnspan=3, column=0, row=0)
        tk.Button(self.image_top, command=pressed, text="Save Image").grid(column=0, row=1)
        self.image_top.transient(config.Root_obj)
