
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import radiotest.config.config as config
import radiotest.config.configdata as configdata
import radiotest.drivers.loader as loader
import radiotest.gui.top as gui
import radiotest.tests.harmspur as harmspur_test
import radiotest.tests.imd as imd_test
import radiotest.tests.trxlo as trxlo_test

# Loader initialization

config.Loader_obj = loader.Loader()

# Config initialization

config.Config_obj = configdata.ConfigData("test")
# Populate instrument list in loader
for instrument in config.Config_obj.get_instrument_list():
    config.Loader_obj.add_instrument(instrument["name"], instrument["instrument"])

# GUI initialization

config.Root_obj = tk.Tk()
config.Root_obj.title("RadioTest")
config.App_obj = gui.FullScreenApp(config.Root_obj)
config.App_obj.grid()

# Test initialization

config.HarmSpur_test_obj = harmspur_test.TestHarmSpur()
config.IMD_test_obj = imd_test.TestImd()
config.TRXLO_test_obj = trxlo_test.TestTRXLO()

# Forever loop

config.Root_obj.mainloop()
