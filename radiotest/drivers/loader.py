import importlib
import subprocess

class LoaderError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Loader:
    def __init__(self):
        self.instrument_table = {}
        self.info_cache = {}

    def _ping(self, host):
        """ Private ping function """
        response = subprocess.call(["ping", "-c1", "-W1", host])
        return True if response == 0 else False

    def load(self, name):
        """Load the driver for an instrument"""
        # If driver used previously, return info for that and reset it.
        info = None
        if name in self.info_cache.keys():
            info = self.info_cache[name]
            info["instance"].rst()
            return info

        if name in self.instrument_table.keys():
            info = self.instrument_table[name]
        if info is None:
            raise LoaderError("Instrument {} not found in list of instruments".format(name))

        if info["interface"] == "vxi" and self._ping(info["hostname"]) is False:
            raise LoaderError("Host {} is offline".format(info["hostname"]))

        dot_path = "radiotest.drivers.instruments"+"."+info["interface"]+"."+info["driver"]
        try:
            module_id = importlib.import_module(dot_path)
        except ImportError:
            raise LoaderError("Driver {} could not be imported".format(info["driver"]))
        driver_class = getattr(module_id, info["class_name"])

        instance = None
        try:
            instance = driver_class(info["hostname"])
        except OSError:
            if info["interface"] == "vxi":
                raise LoaderError("Could not connect to host: {}".format(info["hostname"]))
        # Add 2 more keys to the info to make retrieval of the driver instance and name easy
        info["instance"] = instance
        info["name"] = name
        # To avoid multiple loads of the same device, cache them
        self.info_cache[name] = info
        return info

    def add_instrument(self, name, i_type, driver,  class_name, interface="vxi", hostname=None):
        """ Add an instrument to the instrument table"""
        new_inst = dict()
        new_inst["i_type"] = i_type
        new_inst["driver"] = driver
        new_inst["class_name"] = class_name
        new_inst["interface"] = interface
        new_inst["hostname"] = hostname
        self.instrument_table[name] = new_inst

    def get_driver_instance(self, info):
        """Return the driver instance for the info specified """
        return info["instance"]

    def get_instrument_type(self, info):
        """Return the instrument type for the info specified """
        return info["i_type"]

    def get_instrument_hostname(self, info):
        """Return the host name for the info specified """
        return info["hostname"]

    def get_instrument_name(self, info):
        """Return the instrument name for the info specified """
        return info["name"]