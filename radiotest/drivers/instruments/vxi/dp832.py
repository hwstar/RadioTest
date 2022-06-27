from .instrument import Instrument, InstrumentError
import time

class Dp832(Instrument):
    "This class controls a Rigol DP832 lab power supply"

    def rst(self):
        self._write("*RST")

    def __init__(self, resourcehost):

        Instrument.__init__(self, resourcehost)

        iid = self.identify()
        if (iid[0:24] != 'RIGOL TECHNOLOGIES,DP832'):
            raise InstrumentError('Instrument Manufacturer/Model Number Mismatch,  ' + iid)
        self.rst()


    def channel_setup(self, channel=1, voltage=0.5, current=0.1, enabled = False, protection_state = False, protection_current=0.1):
        "Set up the commonly used parameters"
        self.channel_off(channel)
        self.set_voltage(voltage, channel)
        self.set_current(current)
        self.set_protection_current(protection_current)
        if(protection_state):
            self.set_current_protect_on()
        else:
            self.set_current_protect_off()
        if(enabled):
            self.channel_on(channel)

    def channel_select(self, channel=1):
        "Select a channel"
        self._write(':INST CH{channel}'.format(channel=int(channel)))

    def set_voltage(self, voltage=0.5, channel=0):
        "Set voltage"
        if(channel):
            self.channel_select(channel)
        self._write(':VOLT {voltage}'.format(voltage=voltage))

    def set_current(self, current=0.1, channel=0):
        "Set Current"
        if (channel):
            self.channel_select(channel)
        self._write(':CURR {current}'.format(current=current))

    def set_protection_current(self, current=0.5, channel=0):
        "Set Protection Current"
        if (channel):
            self.channel_select(channel)
        self._write(':CURR:PROT {current}'.format(current=current))

    def set_current_protect_off(self, channel=0):
        "Disable current protection feature"
        if (channel):
            self.channel_select(channel)
        self._write(':CURR:PROT:STAT OFF')

    def set_current_protect_on(self, channel=0):
        "Enable current protection feature"
        if (channel):
            self.channel_select(channel)
        self._write(':CURR:PROT:STAT ON')

    def channel_off(self, channel = 1):
        "Turn a channel off"
        self._write(':OUTP CH{channel},OFF'.format(channel=channel))

    def channel_on(self, channel = 1):
        "Turn a channel on"
        self._write(':OUTP CH{channel},ON'.format(channel=channel))

    def all_channels_off(self):
        "Turn off all channels"
        for ch in range(1,4):
            self._write(':OUTP CH'+str(ch))

    def get_power(self, channel=0):
        "Return power measurement"
        if (channel):
            self.channel_select(channel)
        return self._ask(":MEAS:POWE?")

    def get_current(self, channel=0):
        "Return current measurement"
        if (channel):
            self.channel_select(channel)
        return self._ask(":MEAS:CURR?")

    def get_voltage(self, channel=0):
        "Return current measurement"
        if (channel):
            self.channel_select(channel)
        return self._ask(":MEAS:VOLT?")


if __name__ == "__main__":
    # Test code


    powersupply = dp832("dp832")
    powersupply.channel_setup(1, 15, 0.5)
    powersupply.channel_setup(2, 15, 0.5)
    powersupply.channel_setup(3, 3.3, 1, False, True, 1.1)

    for channel in range(1,4):
        powersupply.channel_on(channel)
        powersupply.channel_select(3)


    print(powersupply.get_voltage(1))

    powersupply.close()