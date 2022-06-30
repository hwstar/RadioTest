import radiotest.config.config as config


class TestImd:
    def __init__(self):
        self.imd_gui = config.App_obj.tabs.tab_frames["imd"]
        self.imd_gui.register_test_function(self.run)

    def run(self, test_setup):
        # Unpack and format the data passed in
        gui = test_setup["gui_inst"]
        sa = test_setup["instruments"]["sa"]["driver_inst"]
        sa_make = sa.make
        sa_model = sa.model
        sa_serial = sa.sn
        sa_fw = sa.fw
        arb = test_setup["instruments"]["awg"]["driver_inst"]
        arb_make = arb.make
        arb_model = arb.model
        arb_serial = arb.sn
        arb_fw = arb.fw
        ref_offset = test_setup["parameters"]["ref_offset"]
        tone_level = test_setup["parameters"]["tone_level"]
        display_line = test_setup["parameters"]["display_line"]
        f1 = test_setup["parameters"]["f1"] * 1E6  # Convert to Hz
        f2 = test_setup["parameters"]["f2"] * 1E6  # Convert to Hz
        span = test_setup["parameters"]["span"] * 1E3  # Convert to Hz

        pass

