from .instrument import Instrument, InstrumentError
import time

class Dsa815(Instrument):
    """This class controls a Rigol DSA815 spectrum analyzer"""

    def rst(self):
        self._write("*RST")

    def __init__(self, resourcehost):
        Instrument.__init__(self, resourcehost)
        self.iid = self.identify()
        if(self.iid[0:25] != 'Rigol Technologies,DSA815'):
            raise InstrumentError('Instrument Manufacturer/Model Number Mismatch, '+self.iid)
        self.make, self.model, self.sn, self.fw = [self.iid.split(",")[i] for i in range(0, 4)]
        self.rst()

    def write(self, message):
        """ Write a command to the DSA815 """
        # DSA815 quirk: Override write method to wait for command completion after every write command
        super().write(message)
        self.wait()


    def console(self):
        """Debugging console"""
        self._console("Rigol Dsa815")

    def sys_preset(self, type="FACT"):
        """Execute a System preset"""
        if type not in ["FACT", "USER1", "USER2", "USER3", "USER4", "USER5", "USER6"]:
            raise InstrumentError("Invalid system preset")
        self.write(":SYST:PRES:TYP: {type}".format(type=type))

    def set_single_sweep(self):
        self.write(':INIT:CONT OFF')

    def set_continuous_sweep(self):
        self.write(':INIT:CONT ON')

    def sweep_restart(self):
        self.write('INIT:REST')

    def trigger_single_sweep(self):
        self.write(':INIT:IMM')

    def set_sweep_accuracy(self, accuracy):
        """Set the sweep accuracy"""
        if accuracy not in ["NORM", "ACC"]:
            raise InstrumentError("Invalid sweep accuracy")
        self.write(":SENS:SWE:TIME:AUTO:RUL:"+accuracy)

    def set_span(self, span):
        """Set the frequency span"""
        self.write(':SENS:FREQ:SPAN '+str(span))

    def set_start_freq(self, start):
        self.write(':SENS:FREQ:START ' + str(start))

    def set_stop_freq(self, stop):
        self.write(':SENS:FREQ:STOP ' + str(stop))

    def set_center_freq(self, center):
        """Set the center frequency"""
        self.write(':SENS:FREQ:CENT '+str(center))

    def set_atten(self, atten):
        """Set the input attenuator"""
        if(atten == "auto"):
            self.write(':SENS:POW:RF:ATT:AUTO ON')
        else:
            self.write(':SENS:POW:RF:ATT '+str(atten))

    def set_ref_level(self, ref_level):
        """ Set the reference level"""
        self.write(':DISP:WIN:TRAC:Y:SCAL:RLEV {ref_level}'.format(ref_level=ref_level))

    def set_ref_offset(self, ref_offset):
        """ Set the reference offset"""
        self.write(':DISP:WIN:TRAC:Y:SCAL:RLEV:OFFS {ref_offset}'.format(ref_offset=ref_offset))


    def set_rbw(self, bw):
        """Set Resolution Bandwidth"""
        self.write(":SENS:BAND:RES {bw}".format(bw=bw))

    def set_vbw(self, bw):
        """Set Video Bandwidth"""
        self.write(":SENS:BAND:VID {bw}".format(bw=bw))
        pass

    def get_peak_data(self):
        """Get the peak data from the peak table"""
        return self.ask(":TRAC:MATH:PEAK:DATA?")

    def get_peak_points(self):
        """ Get the number of points in the peak table"""
        return self.ask(":TRAC:MATH:PEAK:POIN?")

    def set_peak_table_state(self, state):
        """ Enable or disable the peak tablt state"""
        st = "ON" if state is True else "OFF"
        self.write(":TRAC:MATH:PEAK:TABL:STAT {st}".format(st=st))

    def set_peak_table_threshold(self, method="NORM"):
        """ Set the peak table sorting method"""
        self.write(":TRAC:MATH:PEAK:THR {method}".format(method=method))

    def set_peak_table_sort(self, method="FREQ"):
        """ Set the peak table sorting method"""
        self.write(":TRAC:MATH:PEAK:TABL:SORT {method}".format(method=method))

    def set_display_line(self, level=0):
        """ Set the display line"""
        self.write(":DISP:WIN:TRAC:Y:DLIN {level}".format(level=level))

    def set_preamp_off(self):
        """Disable the built in preamp"""
        self.write(':SENS:POW:RF:GAIN OFF')

    def set_preamp_on(self):
        """Enable the built in preamp"""
        self.write(':SENS:POW:RF:GAIN ON')

    def save_screendump(self, file):
        """Save a .bmp screenshot to a file"""
        # Get cont mode
        contmode = self.ask(':INIT:CONT?')
        # Set cont mode off
        self.write(':INIT:CONT 0')
        # Retrieve the header and data for the snapshot
        res = self._ask_read_raw(':PRIV:SNAP?')

        # Split the header and data into separate arrays
        header = res[0:11]
        data = res[11:]
        # Get size from header
        size = int(header[2:])
        # Open the file to write the bitmap info into
        f = open(file, "wb")
        # Write the bitmap info into the file
        f.write(data)
        # Set the file size to what was sent in the header
        f.truncate(size)
        # Close the file
        f.close()
        # Restore the previous cont mode state
        self._write(':INIT:CONT {contmode}'.format(contmode=contmode))
        # Set local mode
        self._write(':SYST:COMM:BRMT 0')
        return


if __name__ == "__main__":
    specan = dsa815("dsa815")
    print(specan.identify())

    specan.set_atten(0)
    specan.set_preamp_off()
    specan.set_center_freq(440E6)
    specan.set_span(20E6)
    specan.save_screendump('/tmp/dsa815.bmp')





    specan.close()

