import math

class TestSupport:
    def __init__(self):
        self.gui = None
        self.sa = None
        self.awg = None
        self.ref_offset = 0
        self.display_line = 0
        self.fundamental = 0
        self.highest_harmonic = 0
        self.test_data = dict()
        self.operating_freq = 0
        self.lo_level = 0
        self.if_carr_freq = 0
        self.usb = False
        self.lo_swap = False
        self.ptt = False

    def sa_make_measurement(self, center_freq, span=100E6, rbw=1000, vbw=1000,
                         ref_offset=40, display_line=10, screen_dump_file=None):
        """ Set up and make a measurement"""
        self.sa.rst()
        self.sa.set_single_sweep()
        self.sa.set_center_freq(center_freq)
        self.sa.set_span(span)
        self.sa.set_ref_level(0.0)
        self.sa.set_ref_offset(ref_offset)
        self.sa.set_rbw(int(rbw))
        self.sa.set_vbw(int(vbw))
        self.sa.set_display_line(display_line)
        self.sa.set_sweep_accuracy("NORM")
        self.sa.set_peak_table_sort("FREQ")
        self.sa.set_peak_table_threshold("DLM")
        self.sa.set_peak_table_state(True)
        self.sa.trigger_single_sweep()

        # Get the data
        self.sa.trigger_single_sweep()
        points_str = None
        points = int(self.sa.get_peak_points())
        # Only attempt to retrieve the data if there are one or more peaks present.
        # Not doing this will cause the get_peak_data() method to hang and the Rigol DSA-815 spectrum
        # analyzer will need to be power cycled.
        if points > 0:
            points_str = self.sa.get_peak_data()
        # If a screen dump file has been specified, then get that data now.
        if screen_dump_file is not None:
            self.sa.save_screendump(screen_dump_file)
        # Reset the spectrum analyzer
        self.sa.rst()

        # If there are no data points, return to the caller
        if points_str is None:
            return None

        # Process the received data
        raw_points = points_str.split(",")
        raw_points = [float(x) for x in raw_points]  # Convert everything to floats
        # Retrieve the frequencies of the peaks
        freqs = raw_points[0::][::2] # Even values
        # Retrieve the amplitudes of the peaks
        amplitudes = raw_points[1::][::2] # Odd values
        res = dict()
        res["freqs"] = freqs
        res["amplitudes"] = amplitudes
        return res

    def sa_fund_power(self, measurement_data, fund_freq):
        """Retrieve the power of the fundamental"""
        fund_power = None
        if measurement_data is not None:
            for result in measurement_data["freqs"]:
                i = measurement_data["freqs"].index(result)
                if result == fund_freq:
                    fund_power = measurement_data["amplitudes"][i]
                    break
        return fund_power

    def build_harmonic_list(self, fundamental, highest_harmonic):
        """ Build a list of harmonics"""
        harmonic_table = []
        for i in range(2, highest_harmonic + 1):
            harmonic_table.append(i * fundamental)
        return harmonic_table

    def sa_get_spur_set(self, fund_and_harm_table, peak_data):
        """ Return spur set from peak table"""
        spurs = set()
        freqs = peak_data['freqs']
        for freq in freqs:
            # Exact match
            if freq in fund_and_harm_table:
                continue
            spurs.add(freq)
        return spurs

    def dbm_to_vpp(self, dbm, r=50):
        """ convert dbm to volts peak to peak"""
        pmw = 10 ** (dbm / 10)
        vrms = math.sqrt(pmw * (r / 1000))
        return 2 * (math.sqrt(2) * vrms)

    def dbm_to_vp(self, dbm, r=50):
        """ convert dbm to volts peak """
        pmw = 10 ** (dbm / 10)
        vrms = math.sqrt(pmw * (r / 1000))
        return (math.sqrt(2) * vrms)

    def dbm_to_milliwatts(self, dbm):
        """ convert dbm to milliwatts"""
        return 10 ** (dbm / 10)

    def dbm_to_watts(self, dbm):
        """ convert dbm to watts """
        pmw = self.dbm_to_milliwatts(dbm)
        return pmw / 1000.0

    def format_float_as_string(self, value, precision):
        f_string = "{value:." + str(precision) + "f}"
        return f_string.format(value)




