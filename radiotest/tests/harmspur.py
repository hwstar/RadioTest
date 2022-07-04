import radiotest.config.config as config
from radiotest.tests.testsupport import TestSupport


class TestHarmSpur(TestSupport):
    def __init__(self):
        super().__init__()
        self.harmspur_gui = config.App_obj.tabs.tab_frames["harmspur"]
        self.harmspur_gui.register_test_function(self.run)


    def run(self, test_setup):
        """ Run the test"""
        # Unpack and format the data passed in
        self.gui = test_setup["gui_inst"]
        self.sa = test_setup["instruments"]["sa"]["driver_inst"]
        self.ref_offset = test_setup["parameters"]["ref_offset"]
        self.display_line = test_setup["parameters"]["display_line"]
        self.fundamental = test_setup["parameters"]["fundamental"] * 1E6  # Convert to Hz
        self.highest_harmonic = test_setup["parameters"]["highest_harmonic"]


        # Calculate the span from the fundamental to the highest harmonic plus 1 MHz
        span_all_hz = (self.fundamental * self.highest_harmonic) + 1E6

        # Calculate the center frequency
        center_freq_hz = span_all_hz/2

        # Calculate a table of harmonics
        harmonic_table = self.build_harmonic_list(self.fundamental, self.highest_harmonic)

        # Create another table which includes the fundamental and the harmonics
        fund_and_harm_table = [self.fundamental] + harmonic_table

        # *** Test for close-in spurs @+/-250 kHz  which might not have been filtered out by the TRX bandpass filter ***

        measurement_data = dict()
        measurement_data["spurs_500k"] = self.sa_make_measurement(self.fundamental, span=5E5, rbw=1000, vbw=1000,
                                                          ref_offset=self.ref_offset, display_line= self.display_line)

        # Find the power of the fundamental
        fund_power = self.sa_fund_power(measurement_data["spurs_500k"], fund_and_harm_table[0])
        if fund_power is None:
            self.gui.show_error(title="No fundamental Peak",
                               message="Did not see the fundamental frequency in the peak data. Check your setup")
            return

        # *** Test for close-in spurs @+/-1MHz  which might not have been filtered out by the TRX bandpass filter ***

        measurement_data["spurs_2M"] = self.sa_make_measurement(self.fundamental, span=2E6, rbw=1000, vbw=1000,
                                                                  ref_offset=self.ref_offset,
                                                                  display_line=self.display_line)

        # For best accuracy, measure each of the harmonics one by one with a 500 kHz span
        measurement_data["harmonics"] = list()
        for i, harmonic in enumerate(harmonic_table):
            measurement_data["harmonics"].append(self.sa_make_measurement(harmonic_table[i], span=5E5, rbw=1000,
                                                                          vbw=1000, ref_offset=self.ref_offset,
                                                                          display_line=self.display_line))

        # Uncomment for debug
        #measurement_data['spurs_500k']['freqs'].append(6.123456)
        #measurement_data['spurs_500k']['amplitudes'].append(19.1234)

        # *** Data processing ***
        processed_data = dict()

        # Process the two spur lists
        spur_set_500k = self.sa_get_spur_set(fund_and_harm_table, measurement_data['spurs_500k'])
        spur_set_2M = self.sa_get_spur_set(fund_and_harm_table, measurement_data['spurs_2M'])

        close_in_spurs = spur_set_500k
        close_in_spurs.union(spur_set_2M)
        # Eliminate the fundamental
        if self.fundamental in close_in_spurs:
            close_in_spurs.remove(self.fundamental)
        # Convert spurs to relative power and save in the processed data
        processed_data["spurs_dBc"] = list()
        for freq in close_in_spurs:
            if freq in measurement_data['spurs_500k']['freqs']:
                index = measurement_data['spurs_500k']['freqs'].index(freq)
                processed_data['spurs_dBc'].append(
                    {"MHz": freq, "dBc":-abs(measurement_data['spurs_500k']['amplitudes'][index] - fund_power)})
            elif freq in measurement_data['spurs_2M']['freqs']:
                index = measurement_data['spurs_2M']['freqs'].index(freq)
                processed_data['spurs_dBc'].append(
                    {"MHz": freq, "dBc": -abs(measurement_data['spurs_500k']['amplitudes'][index] - fund_power)})

        # Convert harmonics to relative power and save the processed data
        processed_data["harmonics_dBc"] = list()
        for peaks in measurement_data["harmonics"]:
            if peaks is not None:
                for freq in peaks["freqs"]:
                    if freq in harmonic_table:
                        index = peaks["freqs"].index(freq)
                        amplitude = peaks["amplitudes"][index]
                        info = {"MHz": freq, "dBc": -abs(amplitude - fund_power)}
                        processed_data["harmonics_dBc"].append(info)
        pass