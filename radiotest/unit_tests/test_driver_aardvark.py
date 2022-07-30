import os
import sys
import importlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

cdpkg = importlib.import_module("radiotest.config.configdata")
lpkg = importlib.import_module("radiotest.drivers.loader")

# Loader initialization

Loader_obj = lpkg.Loader()
ConfigData_obj = cdpkg.ConfigData("test")


# Initialize instruments

for instrument in ConfigData_obj.get_instrument_list():
    Loader_obj.add_instrument(instrument["name"], instrument["instrument"])

aardvark = Loader_obj.load("AV")

instance = aardvark["instance"]

devices = instance.get_available_devices()

instance.open(devices[0])

instance.configure(devices[0])

instance.gpio_set_direction(devices[0], "SS", "OUTPUT")

instance.gpio_set_output(devices[0], "SS", True)

instance.close_all()




