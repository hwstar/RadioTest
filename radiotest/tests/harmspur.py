from datetime import datetime
import radiotest.config.config as config
from radiotest.tests.testsupport import TestSupport


class TestHarmSpur(TestSupport):
    def __init__(self):
        super().__init__()
        self.harmspur_gui = config.App_obj.tabs.tab_frames["harmspur"]
        self.harmspur_gui.register_test_function(self.run)


    def run(self, test_setup):
        """ Run the test"""
        self.start_time = datetime.now()
        # Unpack and format the data passed in
        self.gui = test_setup["gui_inst"]
        self.sa = test_setup["instruments"]["sa"]["driver_inst"]
        self.project_name = test_setup["parameters"]["project_name"]
        self.test_id = test_setup["parameters"]["test_id"]
        self.ref_offset = test_setup["parameters"]["ref_offset"]
        self.display_line = test_setup["parameters"]["display_line"]
        self.fundamental = test_setup["parameters"]["fundamental"] * 1E6  # Convert to Hz
        self.highest_harmonic = test_setup["parameters"]["highest_harmonic"]
        self.use_awg = test_setup["parameters"]["use_awg"]
        self.harm_screen_dump = test_setup["parameters"]["harm_screenshot"]
        if self.use_awg is True:
            self.awg = test_setup["instruments"]["awg"]["driver_inst"]
            self.tone_level = test_setup["parameters"]["tone_level"]


        # Calculate the span from the fundamental to the highest harmonic plus 1 MHz
        span_all_hz = (self.fundamental * self.highest_harmonic) + 1E6

        # Calculate the center frequency
        center_freq_hz = span_all_hz/2

        # Calculate a table of harmonics
        harmonic_table = self.build_harmonic_list(self.fundamental, self.highest_harmonic)

        # Set up the AWG if enabled
        if self.use_awg is True:
            self.awg.rst()
            # Convert tone level to volts P-P
            tone_vpp = self.dbm_to_vpp(self.tone_level)
            # Set output impedance for channel 1
            self.awg.output_sourcez(1, 50)
            # Set the tone frequency
            # Set the amplitude
            self.awg.sine(1, freq=self.fundamental, amplitude=tone_vpp, offset=0.0, phase=0.0)
            self.awg.output_on(1)

        # Create another table which includes the fundamental and the harmonics
        fund_and_harm_table = [self.fundamental] + harmonic_table

        # *** Test for close-in spurs @+/-250 kHz  which might not have been filtered out by the TRX bandpass filter ***

        measurement_data = dict()
        measurement_data["screen_dumps"] = dict()

        measurement_data["spurs_500k"] = self.sa_make_measurement(self.fundamental, span=5E5, rbw=1000, vbw=1000,
                                                          ref_offset=self.ref_offset, display_line= self.display_line)

        # Find the power of the fundamental
        fund_power = self.sa_fund_power(measurement_data["spurs_500k"], fund_and_harm_table[0])
        if fund_power is None:
            self.gui.show_error(title="No fundamental Peak",
                               message="Did not see the fundamental frequency in the peak data.\
                                Check your setup, and your fundamental frequency parameter")
            return None

        # *** Test for close-in spurs @+/-1MHz  which might not have been filtered out by the TRX bandpass filter ***

        measurement_data["spurs_2M"] = self.sa_make_measurement(self.fundamental, span=2E6, rbw=1000, vbw=1000,
                                                                  ref_offset=self.ref_offset,
                                                                  display_line=self.display_line)

        # For best accuracy, measure each of the harmonics one by one with a 500 kHz span

        measurement_data["harmonics"] = list()
        for i, harmonic in enumerate(harmonic_table):
            measurement_data["harmonics"].append(self.sa_make_measurement(harmonic_table[i], span=5E5, rbw=1000,
                                                                          vbw=1000, ref_offset=self.ref_offset,
                                                                          display_line=self.display_line
                                                                          ))

        # If requested, get a complete screen shot of all the harmonics
        screen_dump_name = "Harmonics Screen Dump" if self.harm_screen_dump is True else None
        if screen_dump_name is not None:
            measurement_data["screen_dumps"]["harmonics"] = (self.sa_make_measurement(center_freq_hz,
                                                                                     span=span_all_hz, rbw=10000,
                                                                                     vbw=10000,
                                                                                     ref_offset=self.ref_offset,
                                                                                     display_line=self.display_line,
                                                                                     screen_dump_name=screen_dump_name
                                                                                     ))


        # Uncomment for debug
        #measurement_data['spurs_500k']['freqs'].append(6.123456)
        #measurement_data['spurs_500k']['amplitudes'].append(19.1234)

        # *** Data processing ***


        # Process the two spur lists
        spur_set_500k = self.sa_get_spur_set(fund_and_harm_table, measurement_data['spurs_500k'])
        spur_set_2M = self.sa_get_spur_set(fund_and_harm_table, measurement_data['spurs_2M'])

        close_in_spurs = spur_set_500k
        close_in_spurs.union(spur_set_2M)
        # Eliminate the fundamental
        if self.fundamental in close_in_spurs:
            close_in_spurs.remove(self.fundamental)
        # Convert spurs to relative power and save in the processed data

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
        #   |        item dict {Name, Make, Model, Serial, Firmware}
        #   |            |
        #   |            ...
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
        test_parameters.append({"Test Name": test_setup["parameters"]["test_name"]})
        test_parameters.append({"Fundamental Frequency": self.fundamental/1E6, "Unit": "MHz"})
        test_parameters.append({"Project Name": self.project_name})
        test_parameters.append({"Test ID": self.test_id})
        test_parameters.append({"Reference Offset": self.ref_offset, "Unit": "dB"})
        test_parameters.append({"Measurement Threshold": self.display_line, "Unit": "dB"})
        test_parameters.append({"Highest Harmonic": self.highest_harmonic})
        use_awg = "YES" if self.use_awg is True else "NO"
        test_parameters.append({"Use AWG": use_awg})
        if self.use_awg is True:
            test_parameters.append({"AWG Tone Level": self.tone_level, "Unit": "dBm"})
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

        # Test results

        processed_data["results"] = list()
        results_table_spurs = list()
        i = 1
        for freq in close_in_spurs:
            if freq in measurement_data['spurs_500k']['freqs']:
                index = measurement_data['spurs_500k']['freqs'].index(freq/1E6)
                results_table_spurs.append(
                    {"Spur": i, "MHz": freq,
                    "Power": self.format_float_as_string(-abs(measurement_data['spurs_500k']['amplitudes'][index] - fund_power), 2), "Unit": "dBc"})
                i += 1
            elif freq in measurement_data['spurs_2M']['freqs']:
                index = measurement_data['spurs_2M']['freqs'].index(freq/1E6)
                results_table_spurs.append(
                    {"Spur": i, "MHz": freq,
                    "Power": self.format_float_as_string(-abs(measurement_data['spurs_500k']['amplitudes'][index] - fund_power), 2), "Unit": "dBc"})
                i += 1
        # Append legend and results table

        processed_data["results"].append({"Spurious Emissions": results_table_spurs})

        # Convert harmonics to relative power and save the processed data
        results_table_harmonics = list()
        for peaks in measurement_data["harmonics"]:
            if peaks is not None:
                for freq in peaks["freqs"]:
                    if freq in harmonic_table:
                        index = peaks["freqs"].index(freq)
                        amplitude = peaks["amplitudes"][index]
                        info = {"Harmonic": harmonic_table.index(freq)+2, "Freq(MHz)": freq/1E6,
                                "Power": self.format_float_as_string(-abs(amplitude - fund_power), 2), "Unit": "dBc"}
                        results_table_harmonics.append(info)
        # Append legend and results table
        processed_data["results"].append({"Harmonics": results_table_harmonics})

        results_table_output_power = list()
        results_table_output_power.append({"Output Power (dBm)": self.format_float_as_string(fund_power, 2),
                                           "Unit": "dBm"})
        results_table_output_power.append({"Output Power (W)": self.format_float_as_string(self.dbm_to_watts(fund_power), 2),
                                           "Unit": "W"})
        processed_data["results"].append({"Output power": results_table_output_power})

        # if a screenshot was specified, insert it here
        processed_data["screen_dumps"] = list()
        if self.harm_screen_dump is True:
            processed_data["screen_dumps"].append(measurement_data["screen_dumps"]["harmonics"])

        return processed_data


