import radiotest.config.config as config


class TestHarmSpur:
    def __init__(self):
        self.harmspur_gui = config.App_obj.tabs.tab_frames["harmspur"]
        self.harmspur_gui.register_test_function(self.run)

    def run(self, test_setup):
        # Unpack and format the data passed in
        gui = test_setup["gui_inst"]
        sa = test_setup["instruments"]["sa"]["driver_inst"]
        sa_make = sa.make
        sa_model = sa.model
        sa_serial = sa.sn
        sa_fw = sa.fw
        ref_offset = test_setup["parameters"]["ref_offset"]
        display_line = test_setup['parameters']["display_line"]
        fundamental = test_setup['parameters']['fundamental'] * 1E6  # Convert to Hz
        highest_harmonic = test_setup['parameters']['highest_harmonic']


