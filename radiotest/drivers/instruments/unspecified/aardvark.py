import aardvark_py as apy
import radiotest.error_handling.exceptions as rte




class Aardvark:

    def __init__(self, serial):
        pass


    def _apy_error(self, code):
        """
        Raise an aardvark_py exception
        :param code:  Error code returned by aardvark_py
        :return: Bothing
        """
        error_code_string = apy.aa_status_string(code)
        if isinstance(error_code_string, str):
            raise rte.DriverError("Aardvark_py API error: {}".format(error_code_string))
        else:
            raise rte.DriverError("Aardvark_py API error: {}".format(code))


    def get_available_devices(self):
        """
        :return:  Return a list of available devices
        """
        (res, devarray) = apy.aa_find_devices(4)
        if res < 0:
            raise rte.DriverError(res)
        all_devices = devarray[1]
        device_list = list()
        for device in all_devices:
            if device & 0x8000:
                continue
            serial = apy.aa_unique_id(device)
            if serial < 0:
                self._apy_error(res)
            version = apy.aa_version(device)
            if version < 0:
                self._apy_error(version)
            device_list.append({"device": device, "serial": serial, "version": version, 'handle':None})
        return device_list


    def rst(self):
        # Required but not used.
        pass





