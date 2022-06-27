from .instrument import instrument, InstrumentError

class Sdm3055(instrument):
    """This class controls a Siglent SDM3055 bench DVM"""
    def __init__(self, resourcehost):

        instrument.__init__(self,resourcehost)

        iid = self.identify()
        if (iid[0:27] != 'Siglent Technologies, ,SDM3'):
            raise InstrumentError('Instrument Manufacturer/Model Number Mismatch,  '+iid)


    def measure_voltage(self, acdc='DC', mrange='auto'):
        """Measure voltage"""
        return self._ask('MEAS:VOLT:'+acdc.upper()+'? '+ mrange.upper())

    def measure_current(self, acdc='DC', mrange='auto'):
        """Measure current"""
        return self._ask('MEAS:CURR:' + acdc.upper() + '?'+ mrange.upper())

    def measure_2wire_resistance(self, mrange='auto'):
        """Measure 2 wire resistance"""
        return self._ask('MEAS:RES? '+mrange.upper())

    def measure_4wire_resistance(self, mrange='auto'):
        """Measure 4 wire resistance"""
        return self._ask('MEAS:FRES? '+mrange.upper())

    def measure_capacitance(self,mrange='auto'):
        """Measure capacitance"""
        return self._ask('MEAS:CAP? ' + mrange.upper())

    def measure_diode(self):
        """Measure diode"""
        return self._ask('MEAS:DIOD?')

    def measure_frequency(self):
        """Measure frequency"""
        return self._ask('MEAS:FREQ?')

    def console(self):
        """Enter text console"""
        self._console("Siglent SDM3055")



if __name__ == "__main__":


    dvm = sdm3055("sdm3055")

    print(dvm.measure_voltage())

    dvm.close()