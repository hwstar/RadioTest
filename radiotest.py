
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import radiotest.config.config as config
import radiotest.config.configdata as configdata
import radiotest.drivers.loader as loader
import radiotest.gui.classes as gui

# Loader initialization

config.Loader_obj = loader.Loader()

# Config initialization

config.Config_obj = configdata.ConfigData("test")
# Populate instrument list in loader
for instrument in config.Config_obj.get_instrument_list():
    config.Loader_obj.add_instrument(instrument["name"], instrument["instrument"])

# GUI initialization

Root = tk.Tk()
Root.title("RadioTest")
config.App_obj = gui.FullScreenApp(Root)
config.App_obj.pack(side="top", fill="both", expand=True)

Root.mainloop()
