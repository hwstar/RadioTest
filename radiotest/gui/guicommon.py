import tkinter as tk
import tkinter.ttk as ttk
import io
import csv
import pathlib
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, askyesno
from tkinter.filedialog import asksaveasfile
import radiotest.config.config as config
import radiotest.drivers.loader as loader


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

    def number_listbox_create(self, row, label, start, end, default=None, step=1, height=4):
        """
        Create a list box

        :param row: Row number to place list box on
        :param label: Text label for listboc
        :param start:  starting number
        :param end:  ending number
        :param default: default value to select
        :param step: skip value between numbers
        :param height: listbox height

        :return:
        data structure to be used to retrieve the selection
        """
        tk.Label(self, text=label).grid(row=row, column=0)
        widget = tk.Listbox(self, selectmode=tk.SINGLE, width=4, height=height)
        widget.grid(row=row, column=1)
        selection_map = list()
        for index,list_number in enumerate(range(start, end + 1, step)):
            ls = str(list_number)
            widget.insert(index, ls)
            selection_map.append(ls)

        if default is not None:
            if str(default) not in selection_map:
                raise ValueError("Invalid default value")
            else:
                selindex = selection_map.index(str(default))
                widget.select_set(selindex)

        return {"widget": widget, "map": selection_map}

    def numbered_radiobuttons_create(self, row, label, intvar, start, end, default=None, step=1):
        """
        Create a list box

        :param row: Row number to place list box on
        :param label: Text label for listboc
        :param start:  starting number
        :param end:  ending number
        :param default: default value to select
        :param step: skip value between numbers


        :return:
        Nothing
        """
        tk.Label(self, text=label).grid(row=row, column=0)

        for i,b in enumerate(range(start, end+1, step)):
            rb = tk.Radiobutton(self, text=str(b), variable=intvar, value=b)
            rb.grid(row=row, column=i+1)


    def number_listbox_get(self, item):
        """
        Get the list box item selected

        :param item: data structure returned by number_listbox_create()
        :return: integer representing the selected item, or None if an item was not selected
        """
        widget = item["widget"]
        map = item["map"]
        cs = widget.curselection()
        if len(cs) == 0:
            return None
        index = cs[0]
        res = int(map[index])
        return res

    def save_results_to_csv(self, the_file, processed_data):
        """
        Save the test results to a .csv file
        :param the_file:  The path and file to save the results to
        :param processed_data:  The test results
        :return:
        Nothing
        """
        def write_row(csv_writer, section, info):
            """

            :param csv_writer: Writer object
            :param section: Section name
            :param info: Information to write
            :return:
            Nothing
            """
            fields = list()
            for key, value in info.items():
                fields.append(key)
                fields.append(str(value))
            row = [section] + fields
            csv_writer.writerow(row)

        def write_row_results(csv_writer, section, results):
            """
            Write multiple rows for each test result
            :param csv_writer:  Writer object
            :param section:  Section name
            :param results:  Results information
            :return:
            Nothing
            """
            description = list(results.keys())[0]

            results_info = results[description]
            for res in results_info:
                fields = list()
                fields.append(section)
                fields.append(description)
                for key, value in res.items():
                    fields.append(key)
                    fields.append(str(value))
                csv_writer.writerow(fields)

        # Create the file
        with open(the_file, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=",")

            # Write test metrics
            for metric in processed_data["test_metrics"]:
                write_row(writer, "Test Metrics", metric)
            # Write the test equipment
            for instrument in processed_data["test_equipment"]:
                write_row(writer, "Test Equipment", instrument)
            # Test parameters
            for parameter in processed_data["test_parameters"]:
                write_row(writer, "Test Parameters", parameter)
            # Test results
            for result in processed_data["results"]:
                write_row_results(writer, "Test Results", result)

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

    def test_parameter_search(self, key, test_parameters):
        """

        :param key: The search key
        :param test_parameters: The test parameters to search
        :return: The test parameter value
        """
        for parameter in test_parameters:
            keys = list(parameter.keys())
            if keys[0] == key:
                res = list(parameter.values())[0]
                return res
        raise KeyError("No Key found in test_parameter_search()")

    def build_file_save_path(self, path_obj, test_parameters):
        """
        :param path_obj: A pathlib object containing leftmost part of the directory path
        :param test_parameters: The test parameters
        :return: A string with the complete directory name
        """
        pd = path_obj / self.test_parameter_search("Project Name", test_parameters) / \
             self.test_parameter_search("Test Name", test_parameters)

        return pd



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

        def show_equipment(row_in):
            """
            This internal function handles displaying the test parameters
            It is passed the starting row, and it returns the next row which can be used
            """
            instruments = processed_data["test_equipment"]
            # Format test parameters
            heading = tk.Label(self.results_top, width=30,
                               text="Test Equipment", font="bold", anchor="w")
            heading.grid(row=row_in, column=0)

            row_in += 1
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Type", font="TkHeadingFont").grid(row=row_in, column=0, sticky=tk.NSEW)
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Make", font="TkHeadingFont").grid(row=row_in, column=1, sticky=tk.NSEW)
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Model", font="TkHeadingFont").grid(row=row_in, column=2, sticky=tk.NSEW)
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Serial", font="TkHeadingFont").grid(row=row_in, column=3, sticky=tk.NSEW)
            tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                     width=30, text="Firmware", font="TkHeadingFont").grid(row=row_in, column=4, sticky=tk.NSEW)

            row_in += 1
            for instrument in instruments:
                values = list(instrument.values())

                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=values[0]).grid(row=row_in, column=0, sticky=tk.NSEW)
                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=values[1]).grid(row=row_in, column=1, sticky=tk.NSEW)
                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=values[2]).grid(row=row_in, column=2, sticky=tk.NSEW)
                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=values[3]).grid(row=row_in, column=3, sticky=tk.NSEW)
                tk.Label(self.results_top, relief=tk.GROOVE, justify=tk.LEFT,
                         width=30, text=values[4]).grid(row=row_in, column=4, sticky=tk.NSEW)
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


        # Save to CSV callback
        def save_to_csv():
            """
            Saves the test data to acsv file
            :return:
            Nothing
            """

            # Expand path (posix)
            pp = pathlib.Path(config.Default_test_results_path)
            pp = pp.expanduser()


            # Generate path to file

            directory = str(self.build_file_save_path(pp, processed_data["test_parameters"]))

            # Generate file name

            file = self.test_parameter_search("Test ID", processed_data["test_parameters"])

            # Make directory if it doesn't exist
            # Ask first
            path = pathlib.Path(directory)
            if not path.exists():
                if(askyesno("Directory does not exist", "Create Directory: {}?".format(directory))):
                    path.mkdir(parents=True)

            #
            # Allow the user to change the path
            #

            filepath = tk.filedialog.asksaveasfilename(parent=self.results_top,
                                 title="Save Test Results",
                                 initialdir=directory,
                                 initialfile=file,
                                 defaultextension=".csv")

            #
            # Save to CSV file
            #
            self.save_results_to_csv(filepath, processed_data)

        def present_image(image_data):
            """
            Present image to user and give them the opportunity to save the image as a file
            :param image_data: Data to show on screen
            :return: Nothing
            """

            def pressed():
                """
                This gets called when the user presses the save image file button
                :return: Nothing
                """
                # Expand path (posix)
                pp = pathlib.Path(config.Default_test_results_path)
                pp = pp.expanduser()

                # Get the path and file name
                directory = str(self.build_file_save_path(pp, processed_data["test_parameters"]))
                file = self.test_parameter_search("Test ID", processed_data["test_parameters"])
                # Make directory if it doesn't exist
                # Ask first
                path = pathlib.Path(directory)
                if not path.exists():
                    if (askyesno("Directory does not exist", "Create Directory: {}?".format(directory))):
                        path.mkdir(parents=True)

                #
                # Allow the user to change the path
                #

                filepath = tk.filedialog.asksaveasfilename(parent=self.results_top,
                                                           title="Save Test Results",
                                                           initialdir=directory,
                                                           initialfile=file,
                                                           defaultextension=".bmp")

                #
                # Save the image to a file
                #
                with open(filepath, "wb") as image_file:
                    image_file.write(dump["data"])


            pil_image = Image.open(io.BytesIO(dump["data"]))
            self.image_top = tk.Toplevel(config.Root_obj)
            self.image_top.title(dump["name"])
            self.python_photo_image = ImageTk.PhotoImage(pil_image)
            self.image_top_label = tk.Label(self.image_top, image=self.python_photo_image)
            self.image_top_label.grid(columnspan=3, column=0, row=0)
            tk.Button(self.image_top, command=pressed, text="Save Image").grid(column=0, row=1)
            self.image_top.transient(config.Root_obj)



        self.results_top = tk.Toplevel(config.Root_obj)
        self.results_top.title(title)

        row = 0

        # Show test metrics

        row = show_results_test_metrics(row)

        # Show test equipment

        row = show_equipment(row)

        # Show test parameters

        row = show_results_test_parameters(row)

        # Show result sets

        for result in processed_data["results"]:
            row = show_results_info(row, result)

        # Show results separator

        row += 1
        results_sep = ttk.Separator(self.results_top, orient=tk.HORIZONTAL)
        results_sep.grid(row=row, column=0, columnspan=10, sticky='ew')

        # Show data disposition
        row += 1
        heading = tk.Label(self.results_top, width=30,
                           text="Data Disposition", font="bold", anchor="w")
        heading.grid(row=row, column=0)

        # Show Save Data to csv button
        row += 1
        column = 0
        save_data_b = tk.Button(self.results_top, text="Save Data to .csv", command=save_to_csv)
        save_data_b.grid(row=row, column=column, sticky="NSEW")

        # Show Screen dump buttons if screen dumps were taken
        column += 1
        for dump in processed_data["screen_dumps"]:

            button = tk.Button(self.results_top,text=dump["name"], command=lambda: present_image(dump))
            button.grid(row=row, column=column, sticky="NSEW")

        # Present window

        self.results_top.transient(config.Root_obj)
