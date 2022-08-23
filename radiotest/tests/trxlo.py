import radiotest.config.config as config
from radiotest.tests.testsupport import TestSupport


class TestTRXLO(TestSupport):
    def __init__(self):
        super().__init__()
        self.trxlo_gui = config.App_obj.tabs.tab_frames["trxlo"]
        self.trxlo_gui.register_test_function(self.run)


    def run(self, test_setup):
        """ Run the test"""
        # Unpack and format the data passed in
        self.gui = test_setup["gui_inst"]
        self.awg = test_setup["instruments"]["awg"]["driver_inst"]
        self.operating_freq = test_setup["parameters"]["operating_freq"] * 1E6
        self.if_carr_freq = test_setup["parameters"]["if_carr_freq"] * 1E6
        self.lo_level = test_setup["parameters"]["lo_level"]
        self.usb = test_setup["parameters"]["usb"]
        self.lo_swap = test_setup["parameters"]["lo_swap"]
        self.ptt = test_setup["parameters"]["ptt"]
        self.tune = test_setup["parameters"]["tune"]

        # If we are using the aardvark, and it was not opened previously, set it up.
        if self.av_inst is None:
            self.av_dict = test_setup["instruments"]["av"] if "av" in test_setup["instruments"] else None
            if self.av_dict:
                self.av_inst = self.av_dict["instance"]
                self.av_device = self.av_inst.get_available_devices()[0]
                # Open first device
                self.av_inst.open(self.av_device)
                # Set GPIO mode
                self.av_inst.configure(self.av_device, device_mode="GPIO_ONLY")
                # Set the pin direction
                self.av_inst.gpio_set_direction(self.av_device, "SCLK", "OUTPUT")  # SS-> PTT
                self.av_inst.gpio_set_direction(self.av_device, "MOSI", "OUTPUT")  # MOSI-> TUNE
                self.av_inst.gpio_set_direction(self.av_device, "MISO", "OUTPUT")  # MISO-> MUTE

        if self.av_device:
            # Set the pin state
            self.av_inst.gpio_set_output(self.av_device, "SCLK", self.ptt)
            self.av_inst.gpio_set_output(self.av_device, "MISO", self.ptt)
            tune_val = True  if self.ptt and self.tune else False
            self.av_inst.gpio_set_output(self.av_device, "MOSI", tune_val)

        # Calculate
        # If in LSB mode, we need to ensure the low side injection frequency is always positive
        diff_freq = self.if_carr_freq - self.operating_freq if self.if_carr_freq > self.operating_freq else \
            self.operating_freq - self.if_carr_freq
        injection_frequency = (self.operating_freq + self.if_carr_freq)\
            if self.usb is True else diff_freq

        if self.ptt is True:
            if self.lo_swap is True:
                output_a_freq = self.if_carr_freq
                output_b_freq = injection_frequency
            else:
                output_a_freq = injection_frequency
                output_b_freq = self.if_carr_freq
        else:
            output_a_freq = injection_frequency
            output_b_freq = self.if_carr_freq

        # Setup the AWG
        self.awg.rst()
        self.awg.output_sourcez(1, 50)
        self.awg.output_sourcez(2, 50)
        lo_vpp = self.dbm_to_vpp(self.lo_level)
        self.awg.sine(channel=1, freq=output_a_freq, amplitude=lo_vpp, offset=0.0, phase=0.0)
        self.awg.sine(channel=2, freq=output_b_freq, amplitude=lo_vpp, offset=0.0, phase=0.0)
        self.awg.output_on(1)
        self.awg.output_on(2)

        return None
