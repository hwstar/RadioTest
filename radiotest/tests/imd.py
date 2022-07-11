import time
from datetime import datetime
import radiotest.config.config as config
from radiotest.tests.testsupport import TestSupport


class TestImd(TestSupport):
    def __init__(self):
        super().__init__()
        self.imd_gui = config.App_obj.tabs.tab_frames["imd"]
        self.imd_gui.register_test_function(self.run)




    def run(self, test_setup):
        self.start_time = datetime.now()
        # Unpack and format the data passed in
        self.gui = test_setup["gui_inst"]
        self.sa = test_setup["instruments"]["sa"]["driver_inst"]
        self.awg = test_setup["instruments"]["awg"]["driver_inst"]
        self.project_name = test_setup["parameters"]["project_name"]
        self.test_id = test_setup["parameters"]["test_id"]
        self.ref_offset = test_setup["parameters"]["ref_offset"]
        self.tone_level = test_setup["parameters"]["tone_level"]
        self.display_line = test_setup["parameters"]["display_line"]
        self.f1 = test_setup["parameters"]["f1"] * 1E6  # Convert to Hz
        self.f2 = test_setup["parameters"]["f2"] * 1E6  # Convert to Hz
        self.max_order = test_setup["parameters"]["max_order"]
        self.imd_screen_dump = test_setup["parameters"]["imd_screenshot"]
        self.two_tone_products = self.build_two_tone_products_list(self.f1, self.f2, self.max_order)

        # Calculate span and center frequency
        tone_delta = abs(self.f1 - self.f2)
        min_max_delta = max(self.two_tone_products["all"]) - min(self.two_tone_products["all"])
        span = tone_delta / 2 + min_max_delta
        center_freq = self.f1 + tone_delta / 2
        #
        # Set up the Arbitrary Waveform Generator
        #

        # Convert tone level to volts P-P
        tone_vpp = self.dbm_to_vpp(self.tone_level)
        # Reset the awg
        self.awg.rst()
        # Set output impedances for channels 1 and 2
        self.awg.output_sourcez(1, 50)
        self.awg.output_sourcez(2, 50)
        # Set the frequencies
        self.awg.sine(1, freq=self.f1, amplitude=tone_vpp, offset=0.0, phase=0.0)
        self.awg.sine(2, freq=self.f2, amplitude=tone_vpp, offset=0.0, phase=0.0)
        # Enable the outputs
        self.awg.output_on(1)
        self.awg.output_on(2)
        # Combine both outputs onto channel 1
        self.awg.channel_combine(True, 1)

        time.sleep(1)
        #
        # Use the spectrum analyzer to make the measurement
        #
        screen_dump_name = "IMD Screen Dump" if self.imd_screen_dump is True else None
        result = self.sa_make_measurement(center_freq,
                                          ref_offset=self.ref_offset,
                                          span=span,
                                          rbw=100,
                                          vbw=100,
                                          display_line=self.display_line,
                                          screen_dump_name=screen_dump_name
                                          )
        # The measurement should have returned a dict with one table of frequencies "freqs"
        # and one table of amplitudes

        # Schema for processed_data
        # processed_data (dict)
        #   |
        #   key results (list)
        #   |  |
        #   |legend, list results map (dict)
        #   |  |                 |
        #   |  |            results_table (list)
        #   |  |                     |
        #   |  |                   table row (dict)
        #   | ...                    |
        #   |                       ...
        #   |
        #   key test_parameters (list)
        #   |           |
        #   |           item dict {Parameter Name, Value, Unit}
        #   |           |
        #   |           ...
        #   |
        #   |
        #   key equipment
        #   |    |
        #   |    type list
        #   |        |
        #   |     item dict {Name, Make, Model, Serial, Firmware}
        #   |            |
        #   |           ...
        #   key screen_dumps (list)
        #       |
        #       screendump(dict) {name, size, data}
        #       |
        #      ...
        #
        #

        # Create top level dict
        processed_data = dict()

        # Test metrics
        test_metrics = list()
        now = datetime.now()
        run_time = str(now - self.start_time)
        test_metrics.append({"Time stamp": self.get_timestamp(now)})
        test_metrics.append({"Run time": run_time})
        processed_data["test_metrics"] = test_metrics

        # Test parameters

        test_parameters = list()
        now = datetime.now()
        run_time = str(now - self.start_time)
        test_parameters.append({"Test Name": test_setup["parameters"]["test_name"]})
        test_parameters.append({"F1": self.f1/1E6, "Unit": "MHz"})
        test_parameters.append({"F2": self.f2/1E6, "Unit": "MHz"})
        test_parameters.append({"Project Name": self.project_name})
        test_parameters.append({"Test ID": self.test_id})
        test_parameters.append({"Reference Offset": self.ref_offset,"Unit": "dB"})
        test_parameters.append({"Measurement Threshold":self.display_line, "Unit": "dB"})
        test_parameters.append({"Tone Level": self.tone_level, "Unit": "dBm"})
        test_parameters.append({"Order": self.max_order})
        processed_data["test_parameters"] = test_parameters


        # Test equipment
        test_equipment = list()
        for key, value in test_setup["instruments"].items():
            item = {"Name": value["name"], "Make": value["driver_inst"].make,
                    "Model": value["driver_inst"].model, "Serial": value["driver_inst"].sn,
                    "Firmware": value["driver_inst"].fw
                    }
            test_equipment.append(item)

        processed_data["test_equipment"] = test_equipment


        # Find F1 and F2, and get their amplitudes
        f1_peak_power = self.sa_get_peak(result, self.f1, 100)

        if f1_peak_power is None:
            self.gui.show_error(title="Measurement Setup Error", message="Did not see a peak for F1 in the measurement data. Check your setup for cabling errors")
            return
        f2_peak_power = self.sa_get_peak(result, self.f2, 100)
        if f2_peak_power is None:
            self.gui.show_error(title="Measurement Setup Error", message="Did not see a peak for F2 in the measurement data. Check your setup for cabling errors")
            return None

        # Establish carrier power
        carrier_power = min(f1_peak_power["amplitude"], f2_peak_power["amplitude"])



        # Retrieve the IMD products from the measurement data, and reference then to the carrier power
        # Test results
        processed_data["results"] = list()
        results_table_products = list()
        for order, freqs in self.two_tone_products["by_product"].items():

            left = self.sa_get_peak(result, freqs[0], 100)

            if left is not None:
                results_table_products.append({"Order": order, 'Freq(MHz)': freqs[0]/1E6,
                                               "Power": self.format_float_as_string(-abs(carrier_power-left["amplitude"]),2), "Unit": "dBc"})

            right = self.sa_get_peak(result, freqs[1], 100)

            if right is not None:
                results_table_products.append({"Order": order, 'Freq(MHz)': freqs[1]/1E6,
                                               "Power": self.format_float_as_string(-abs(carrier_power - right["amplitude"]),2), "Unit": "dBc"})


        if len(results_table_products) == 0:
            self.gui.show_error("No Data", "No IMD products were seen. Check your test setup and test parameters")
            return None




        test_parameters = {"Test Name": test_setup["parameters"]["test_name"]}

        processed_data["results"].append({"IMD Products List": results_table_products})

        # Place f1 and f2 peak power in the test results
        results_table_f1_f2 = list()
        results_table_f1_f2.append({"Freq":"F1", "Output Power": self.format_float_as_string(f1_peak_power["amplitude"], 2), "Unit": "dBm"})
        results_table_f1_f2.append({"Freq":"F2", "Output Power": self.format_float_as_string(f2_peak_power["amplitude"], 2), "Unit": "dBm"})

        processed_data["results"].append({"F1/F2 Output Power": results_table_f1_f2})

        # if a screen dump was specified, insert it here
        processed_data["screen_dumps"] = list()
        if self.imd_screen_dump is True:
            processed_data["screen_dumps"].append(result["screen_dump"])



        return processed_data

