import aardvark_py as apy
import radiotest.error_handling.exceptions as rte




class Aardvark:

    def __init__(self):
        self.device_list = list()
        self.direction = ["INPUT","OUTPUT"]
        self.modes = ["GPIO_ONLY", "SPI_GPIO", "GPIO_I2C", "SPI_I2C"]
        self.pins = ["SCL", "SDA", "MISO", "SCLK", "MOSI", "SS"]
        pass


    def _apy_error(self, code):
        """
        Raise an aardvark_py exception
        :param code:  Error code returned by aardvark_py
        :return: Nothing
        """
        error_code_string = apy.aa_status_string(code)
        if isinstance(error_code_string, str):
            raise rte.DriverError("Aardvark_py API error: {}".format(error_code_string))
        else:
            raise rte.DriverError("Aardvark_py API error: {}".format(code))

    def _handle_check(self, device_info):
        """
        Checks to see that the device info dict has a valid aardvark handle
        :param device_info:  device info dict to check
        :return:  Device handle
        """
        if device_info["handle"] is None:
            raise rte.DriverError("No aardvark handle for device, was the device opened?")
        return device_info['handle']

    def _pin_check(self, pin):
        """
        Checks to see that the device info dict has a valid aardvark handle
        :param pin:  Pin name to check
        :return:  Pin mask bit
        """
        if pin not in self.pins:
            raise rte.DriverError("Invalid pin name specified")
        pin_index = self.pins.index(pin)
        return 1 << pin_index

    def _boolean_check(self, var):
        if var is True or var is False:
            return var
        raise rte.DriverError("Variable should be set to True or False")

    def _direction_check(self, direction):
        """
        Checks to see that the device info dict has a valid aardvark handle
        :param direction:  direction name to check
        :return:  Direction mask bit
        """
        if direction not in self.direction:
            raise rte.DriverError("Invalid direction specified")
        return self.direction.index(direction)



    def get_available_devices(self):
        """
        :return:  Return a list of available devices as one dict per device
        """
        # Find any connected devices
        (res, devarray, unique_ids) = apy.aa_find_devices_ext(1, 1) # Limited to one device for simplicity
        if res < 0:
            self._apy_error(res)
        if len(list(devarray)) == 0:
            raise rte.DriverError("No Aardvark devices detected")
        # Convert (silly) arrays into lists
        all_devices = list(devarray)
        all_unique_ids = list(unique_ids)
        # Build device list
        self.device_list = list()
        for index, device in enumerate(all_devices):
            if device & 0x8000:
                continue
            serial = all_unique_ids[index]
            version = apy.aa_version(device)
            self.device_list.append({"device": device, "serial": serial, 'handle':None})
        # Return the device list
        return self.device_list

    def open(self, device_info):
        """
        Open a particular device using its specific info dict.
        :param device_info: dict of device info
        :return: Nothing
        """

        if device_info["handle"] is not None:
            raise rte.DriverError("Aardvark device {} is already open".format(device_info["device"]))

        device_info["device_mode"] = 0
        device_info["pin_direction"] = 0
        device_info["pin_state"] = 0

        # Open the device
        res = apy.aa_open(device_info["device"])
        if res < 0:
            self._apy_error(res)  # An error occurred
        device_info["handle"] = res

    def close(self, device_info):
        """
        Close an aardvark device
        :param device_info:  Device information for device to close
        :return: Nothing
        """

        if device_info["handle"] is not None:
            apy.aa_close(device_info["handle"])
            device_info["handle"] = None

    def close_all(self):
        """
        Close all aardvark devices
        :return: Nothing
        """
        for device_info in self.device_list:
            self.close(device_info)

    def configure(self, device_info, device_mode="GPIO_ONLY"):
        """
        Configure the Aardvark operating mode
        :param device_info: Device information for device to configure
        :param device_mode:  Device mode string (One of: "GPIO_ONLY", "SPI_GPIO", "GPIO_I2C", or "SPI_I2C")
        :return: Nothing
        """

        handle = self._handle_check(device_info)
        if device_mode not in self.modes:
            raise rte.DriverError("Incorrect Mode: {} specified".format(device_mode))
        device_info["device_mode"] = self.modes.index(device_mode)
        res = apy.aa_configure(handle, device_info["device_mode"])
        if res < 0:
            self._apy_error(res)

        if device_mode == "GPIO_ONLY":
            # Set to all inputs
            res = apy.aa_gpio_direction(handle, device_info["pin_direction"])
            if res < 0:
                self._apy_error(res)
            # Set all outputs low
            res = apy.aa_gpio_set(handle, device_info["pin_state"])
            if res < 0:
                self._apy_error(res)


    def gpio_set_direction(self, device_info, pin, direction):
        """
        Set direction for GPIO pin
        :param device_info: Device information for device to operate on
        :param pin: Pin name string (One of "SCL", "SDA", "MISO", "SCLK", "MOSI", or "SS")
        :param direction: Direction name string (One of "INPUT" or "OUTPUT")
        :return: Nothing

        """
        handle = self._handle_check(device_info)
        pin_mask = self._pin_check(pin)
        pin_direction = self._direction_check(direction)
        if pin_direction: # Output?
            device_info["pin_direction"] |= pin_mask
        else:
            device_info["pin_direction"] &= ~pin_mask
        res = apy.aa_gpio_direction(handle, device_info["pin_direction"])
        if res < 0:
            self._apy_error(res)



    def gpio_set_output(self, device_info, pin, state=False):
        """
        Set the state of an output pin
        :param device_info: Device info for device with desired output pin
        :param state:  Pin state: True = High, False = Low
        :return: Nothing
        """
        self._boolean_check(state)
        handle = self._handle_check(device_info)
        pin_mask = self._pin_check(pin)
        if not state:
            device_info["pin_state"] &= ~pin_mask
        else:
            device_info["pin_state"] |= pin_mask
        res = apy.aa_gpio_set(handle, device_info["pin_state"])
        if res < 0:
            self._apy_error(res)










