import radiotest.config.config as config


class TestImd:
    def __init__(self):
        self.imd_gui = config.App_obj.tabs.tab_frames["imd"]
        self.imd_gui.register_test_function(self.run)
        self.gui = None
        self.sa_driver = None
        self.arb = None
        self.ref_offset = 0
        self.tone_level = 0
        self.display_line = 0
        self.f1 = 0
        self.f2 = 0
        self.span = 10000


    def run(self, test_setup):
        # Unpack and format the data passed in
        self.gui = test_setup["gui_inst"]
        self.sa_driver = test_setup["instruments"]["sa"]["driver_inst"]
        self.arb = test_setup["instruments"]["awg"]["driver_inst"]
        self.ref_offset = test_setup["parameters"]["ref_offset"]
        self.tone_level = test_setup["parameters"]["tone_level"]
        self.display_line = test_setup["parameters"]["display_line"]
        self.f1 = test_setup["parameters"]["f1"] * 1E6  # Convert to Hz
        self.f2 = test_setup["parameters"]["f2"] * 1E6  # Convert to Hz
        self.span = test_setup["parameters"]["span"] * 1E3  # Convert to Hz


