import importlib
import subprocess
import radiotest.error_handling.exceptions as rte


class Loader:
    def __init__(self):
        self.instrument_table = {}
        self.info_cache = {}

    def _ping(self, host):
        """ Private ping function """
        response = subprocess.call(["ping", "-c1", "-W1", host],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True if response == 0 else False

    def load(self, name):
        """Load the driver for an instrument"""
        # If driver used previously return that info. If the interface is vxi, reset it.
        info = None
        if name in self.info_cache.keys():
            info = self.info_cache[name]
            if info["interface"] == "vxi":
                info["instance"].rst()
            return info

        # Search the instrument table for the requested instrument
        if name in self.instrument_table.keys():
            info = self.instrument_table[name]
        if info is None:
            raise rte.LoaderError("Instrument {} not found in list of instruments".format(name))

        # if the instrument interface  is vxi,  perform a test ping
        if info["interface"] == "vxi" and self._ping(info["hostname"]) is False:
            raise rte.LoaderError("Host {} is offline".format(info["hostname"]))

        # Build the dot path to load the driver
        dot_path = "radiotest.drivers.instruments"+"."+info["interface"]+"."+info["driver"]
        try:
            module_id = importlib.import_module(dot_path)
        except ImportError:
            raise rte.LoaderError("Driver {} could not be imported".format(info["driver"]))
        driver_class = getattr(module_id, info["class_name"])

        # Instantiate the instrument
        instance = None
        try:
            # VXI case
            if info["interface"] == "vxi":
                instance = driver_class(info["hostname"])
            # Aardvark case
            elif info["interface"] == "unspecified" and info["driver"] == "aardvark":
                instance = driver_class()

        except (OSError):
            if info["interface"] == "vxi":
                raise rte.LoaderError("Could not connect to host: {}".format(info["hostname"]))
            elif info["interface"] == "unspecified" and info["driver"] == "aardvark":
                raise rte.LoaderError("Could not connect to Aardvark serial number: {}")

        # Add 2 more keys to the info to make retrieval of the driver instance and name easy
        info["instance"] = instance
        info["name"] = name
        # To avoid multiple loads of the same device, cache them
        self.info_cache[name] = info
        return info

    def add_instrument(self, name, instrument):
        """ Add an instrument to the instrument table"""
        self.instrument_table[name] = instrument

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