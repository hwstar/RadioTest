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
        self.ref_offset = test_setup["parameters"]["ref_offset"]
        self.tone_level = test_setup["parameters"]["tone_level"]
        self.display_line = test_setup["parameters"]["display_line"]
        self.f1 = test_setup["parameters"]["f1"] * 1E6  # Convert to Hz
        self.f2 = test_setup["parameters"]["f2"] * 1E6  # Convert to Hz
        self.max_order = test_setup["parameters"]["max_order"]
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
        self.awg.sine(1, self.f1)
        self.awg.sine(2, self.f2)
        # Enable the outputs
        self.awg.output_on(1)
        self.awg.output_on(2)
        # Combine both outputs onto channel 1
        self.awg.channel_combine(True, 1)

        time.sleep(1)
        #
        # Use the spectrum analyzer to make the measurement
        #
        result = self.sa_make_measurement(center_freq,
                                          ref_offset=self.ref_offset,
                                          span=span,
                                          rbw=100,
                                          vbw=100,
                                          display_line=self.display_line,
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
        #       |
        #       type list
        #           |
        #           item dict {Name, Make, Model, Serial, Firmware}
        #               |
        #               ...
        #
        #
        #
        #

        # Create top level dict
        processed_data = dict()



        # Test parameters

        test_parameters = list()
        now = datetime.now()
        run_time = str(now - self.start_time)
        test_parameters.append({"Time stamp": self.get_timestamp(now), "Unit": None})
        test_parameters.append({"Run time": run_time, "Unit": "Seconds"})
        test_parameters.append({"F1": self.f1, "Unit": "MHz"})
        test_parameters.append({"F2": self.f2, "Unit": "MHz"})
        test_parameters.append({"Reference Offset": self.ref_offset,"Unit": "dB"})
        test_parameters.append({"Display Line":self.display_line, "Unit": "dB"})
        test_parameters.append({"Tone Level": self.tone_level, "Unit": "dBm"})
        test_parameters.append({"Order": self.max_order, "Unit": None})

        processed_data["test_parameters"] = test_parameters

        # Test equipment
        test_equipment = list()
        test_equipment.append({"Name": "Spectrum Analyzer", "Make": self.sa.make,
                               "Model": self.sa.model, "Serial": self.sa.sn,
                               "Firmware": self.sa.fw
                               })
        test_equipment.append({"Name": "Arbitrary Waveform Generator", "Make": self.awg.make,
                               "Model": self.awg.model, "Serial": self.awg.sn,
                               "Firmware": self.awg.fw
                               })

        processed_data["test_equipment"] = test_equipment


        # Find F1 and F2, and get their amplitudes
        f1_peak_amplitude = self.sa_get_peak(result, self.f1, 100)

        if f1_peak_amplitude is None:
            self.gui.show_error(title="Measurement Setup Error", message="Did not see a peak for F1 in the measurement data. Check your setup for cabling errors")
            return
        f2_peak_amplitude = self.sa_get_peak(result, self.f2, 100)
        if f1_peak_amplitude is None:
            self.gui.show_error(title="Measurement Setup Error", message="Did not see a peak for F2 in the measurement data. Check your setup for cabling errors")
            return

        # Establish carrier power
        carrier_power = min(f1_peak_amplitude["amplitude"], f2_peak_amplitude["amplitude"])

        # Retrieve the IMD products from the measurement data, and reference then to the carrier power
        # Test results
        processed_data["results"] = list()
        results_table = list()
        for order, freqs in self.two_tone_products["by_product"].items():

            left = self.sa_get_peak(result, freqs[0], 100)

            if left is not None:
                results_table.append({"Order": order, 'Freq': freqs[0],
                                      "Amplitude": -abs(carrier_power-left["amplitude"])})

            right = self.sa_get_peak(result, freqs[1], 100)

            if right is not None:
                results_table.append({"Order": order, 'Freq': freqs[1],
                                      "Amplitude": -abs(carrier_power - right["amplitude"])})


        processed_data["results"].append({"IMD Products List": results_table})

        self.gui.show_results(processed_data)

        pass
