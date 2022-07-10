

# Default Path where test results are saved
Default_test_results_path = "/home/srodgers/projects/test_results"

# Harmonics and spurs defaults

Harm_spurs_defaults = {"fundamental": 7.2, "awg_tone_level": -40,"ref_offset": 40, "highest_harmonic": 7, "display_line": -10}

# IMD Defaults
IMD_defaults = {"ref_offset": 40, "tone_level": -4, "display_line": -10, "f1": 7.2, "f2": 7.2011, "max_order": 7}

# TRX LO Defaults
TRXLO_defaults = {"if_carr_freq": 12.288, "lo_level": 10,
                  "operating_freq": 7.2, "lo_swap": 0, "usb": 0, "ptt": 0 }

# *** Global objects ***
# These are initialized in radiotest.py

# Config

Config_obj = None


# Loader

Loader_obj = None

# GUI
Root_obj = None  # Root Tk obj used by mainloop in radiotest.py
App_obj = None  # Use this to gain access to the GUI methods


# Tests
HarmSpur_test_obj = None
IMD_test_obj = None
TRX_test_obj = None



