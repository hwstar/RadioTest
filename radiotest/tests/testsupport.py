import math
from datetime import datetime

class TestSupport:
    def __init__(self):
        self.gui = None
        self.sa = None
        self.awg = None

        self.start_time = None
        self.tone_level = 0
        self.ref_offset = 0
        self.project_name = 0
        self.test_id = 0
        self.display_line = 0
        self.fundamental = 0
        self.f1 = 0
        self.f2 = 0
        self.max_order = 0
        self.highest_harmonic = 0
        self.two_tone_products = 0
        self.operating_freq = 0
        self.lo_level = 0
        self.tone_level = 0
        self.if_carr_freq = 0
        self.usb = False
        self.lo_swap = False
        self.ptt = False
        self.use_awg = False
        self.harm_screen_dump = False

        self.imd_screen_dump = False

    def sa_make_measurement(self, center_freq, span=100E6, rbw=1000, vbw=1000,
                            ref_offset=40, display_line=10, screen_dump_name=None):
        """ Set up and make a measurement
        Parameters:
            center_freq(float): Center frequency of the measurement in Hz
            span(float): Spectrum anamyzer span to use in Hz
            rbw(int): Spectrum analyzer resolution bandwidth in Hz
            vbw(int): Spectrum analyzer video bandwidth in Hz
            ref_offset(int): The offset used to account for any attenuators between the DUT and the spectrum amalyzer
            display_line(int): Threshold in dB above which peaks will be recorded
            screen_dump_name(str): (optional) A name for the screen dump from the spectrum analyzer

        Returns:
            If peaks were detected, this method returns a dictionary containing 2 tables.
            If no peaks are detected, this method will return None.
            The dictionary keys are "freqs" and "amplitudes". Each contains a list of frequencies or amplitudes.
            """
        res = dict()
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
        if screen_dump_name is not None:
            size, data = self.sa.get_screendump()
            res["screen_dump"] = {"name": screen_dump_name, "size": size, "data": data}
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

        res["freqs"] = freqs
        res["amplitudes"] = amplitudes
        return res

    def sa_fund_power(self, measurement_data, fund_freq):
        """Retrieve the power of the fundamental
        Parameters:
            measurement_data(dict): data from a prior messurement
            fund_freq(float): The fundamental frequency from the the test parameters
        Returns:
            A float if there was a peak at the fundamental, else None
            """
        fund_power = None
        if measurement_data is not None:
            for result in measurement_data["freqs"]:
                i = measurement_data["freqs"].index(result)
                if result == fund_freq:
                    fund_power = measurement_data["amplitudes"][i]
                    break
        return fund_power

    def build_harmonic_list(self, fundamental, highest_harmonic):
        """ Build a list of harmonics
        Parameters:
            fundamental(float): Fundamental frequency in Hz
            highest_harmonic(int) Highest integer harmonic
        Returns:
            list containing all of the harmonics including the highest harmonic

        """
        harmonic_table = []
        for i in range(2, highest_harmonic + 1):
            harmonic_table.append(i * fundamental)
        return harmonic_table

    def build_two_tone_products_list(self, f1, f2, maxorder):
        """ Build a list of 2 tone products
           Parameters:
               f1(float): First tone in Hz
               f2(float): Second tone in Hz
               maxorder(int): Maximum order
           Returns:
               dict containing all of the imd products from third order to max order
        """
        products = dict()

        if maxorder < 3:
            return products
        all_products = list()
        products["by_product"] = dict()
        for i in range(1, int(maxorder/2) + 1):
            product = list()
            a = (i+1)*f1 - i*f2
            b = (i+1)*f2 - i*f1
            product.append(a)
            product.append(b)
            all_products.append(a)
            all_products.append(b)
            products["by_product"][str(i*2+1)] = product
        products['all'] = all_products
        return products

    def sa_get_peak(self, measurement, freq, freq_tol):
        """
        Find a peak at a specific frequency in the measurement table supplied
        Parameters:
            measurement(dict): The data returned from a prior measurement
            freq(float): The frequency of the requested peak
            freq_tol(float): The acceptable tolerance to use when searching the table

        Returns:
            a dict containing the actual frequency, and the amplitude if it exists
            otherwise None

        """
        for i, f in enumerate(measurement['freqs']):
            delta = abs(f-freq)
            if delta <= freq_tol:
                return {"freq": f, "amplitude": measurement['amplitudes'][i]}
        return None





    def sa_get_spur_set(self, fund_and_harm_table, peak_data):
        """ Return spur set from peak table
        Parameters:
            fund_and_harm_table(list): A list of the floating point numbers for the fundamantal and all harmonics
            peak_data(dict): Results from a prior measurement
        Returns:
              A set of spurious frequencies which are not the fundamental or a harmonic
        """

        spurs = set()
        freqs = peak_data['freqs']
        for freq in freqs:
            # Exact match
            if freq in fund_and_harm_table:
                continue
            spurs.add(freq)
        return spurs

    def get_timestamp(self, now):
        return now.strftime("%a, %B %d, %Y, %H:%M:%S")


    def dbm_to_vpp(self, dbm, r=50):
        """ Convert dbm to volts peak to peak
            Parameters:
                dbm(float): The value in dBm to convert
                r(float): The impedance of the system
            Returns:
                A float containing the volt peak to peak
        """
        pmw = 10 ** (dbm / 10)
        vrms = math.sqrt(pmw * (r / 1000))
        return 2 * (math.sqrt(2) * vrms)

    def dbm_to_vp(self, dbm, r=50):
        """ Convert dbm to volts peak
            Parameters:
                dbm(float): The value in dBm to convert
                r(float): The impedance of the system
            Returns:
                A float containing the volt peak
        """
        pmw = 10 ** (dbm / 10)
        vrms = math.sqrt(pmw * (r / 1000))
        return (math.sqrt(2) * vrms)

    def dbm_to_milliwatts(self, dbm):
        """ Convert dbm to milliwatts
            Parameters:
                dbm(float): The value in dBm to convert
            Returns:
                A float representing the equivalent in milliwatts
        """

        return 10 ** (dbm / 10)

    def dbm_to_watts(self, dbm):
        """ Convert dbm to watts
            Parameters:
                dbm(float): The value in dBm to convert
            Returns:
                A float representing the equivalent in watts
        """
        pmw = self.dbm_to_milliwatts(dbm)
        return pmw / 1000.0

    def format_float_as_string(self, value, precision):
        """ Format a floating point number as a string with the supplied precision
        Parameters:
            value(float):   The value to convert to a string
            precision(int): The number of digits to the right of the decimal point to include
        Returns:
            A string representing the number
        """
        f_string = "{value:." + str(precision) + "f}"
        return f_string.format(value=value)




