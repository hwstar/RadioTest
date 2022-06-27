from .instrument import Instrument, InstrumentError

class Mso5000(Instrument):

    """This class controls a RIGOL MSO5000 Scope"""

    def rst(self):
        self._write("*RST")

    def __init__(self, resourcehost):

        Instrument.__init__(self, resourcehost)

        iid = self.identify()
        if not iid.startswith('RIGOL TECHNOLOGIES,MSO50'):
            raise InstrumentError("Instrument Manufacturer/Model Number Mismatch, "+iid)
        self.rst()


    def lock(self, state=False):
        val = 1 if state is True else 0
        self._write(":SYST:LOCK {state}".format(state=val))

    def set_acquire_mem_depth(self, size='AUTO'):
        if size not in ["AUTO","1k","10k,100k","1M","10M","25M","50M","100M","200M"]:
            raise InstrumentError("Invalid acquire memory depth")
        self._write(":ACQ:MDEP {depth}".format(depth=size))
        pass

    def set_channel_display(self, state=True, channel=1):
        st = "ON" if state is True else "OFF"
        self._write(":CHAN{channel}:DISP {st}".format(channel=channel, st=st))

    def set_time_perdiv(self, val=1E-3):
        self._write(":TIM:MAIN:SCAL {scale}".format(scale=val))

    def set_channel_position_calib(self, position=0.0, channel=1):
        self._write(":CHAN{channel}:POS {position}".format(channel=channel, position=position))

    def set_channel_offset(self, offset=0.0, channel=1):
        self._write(":CHAN{channel}:OFFS {offset}".format(channel=channel, offset=offset))

    def set_channel_volts_perdiv(self, val=1.0, chan=1):
        if val not in [0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]:
            raise InstrumentError("Invalid vertical scale value")
        self._write(":CHAN{chan}:SCAL {scale}".format(chan=chan, scale=val))

    def set_channel_invert(self, state=False, channel=1):
        st = "ON" if state is True else "OFF"
        self._write(":CHAN{channel}:INV {st}".format(channel=channel, st=st))

    def set_channel_probe_atten(self, atten=10, chan=1):
        """ Set the probe attenuation"""
        if atten not in [0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000,10000, 20000, 50000]:
            raise InstrumentError("Invalid probe attenuation value")
        self._write(":CHAN{chan}:PROB {atten}".format(chan=chan, atten=atten))

    def set_channel_coup(self, coupling="DC", chan=1):
        if coupling not in ["AC","DC","GND"]:
            raise InstrumentError("Invalid channel coupling value")
        self._write(":CHAN{chan}:COUP {coupling}".format(chan=chan, coupling=coupling))

    def set_channel_bandwidth(self, bw , chan=1):
        if bw not in ["20M", "100M", "200M", "OFF"]:
            raise InstrumentError("Invalid channel bandwidth")
        self._write(":CHAN{chan}:{bw}".format(chan=chan, bw=bw))

    def set_channel_units(self, units="VOLT", chan=1):
        if units not in ["VOLT","VOLTAGE","WATT","AMPERE","AMP","UNKNOWN","UNKN"]:
            raise InstrumentError("Invalid channel unit")
        self._write(":CHAN{channel}:UNIT {units}".format(channel=chan, units=units))

    def run(self):
        self._write(":RUN")

    def stop(self):
        self._write(":STOP")

    def single(self):
        self._write(":SING")

    def set_trigger_mode(self, mode):
        if mode not in ["EDGE","PULSE","PULS","SLOPE","SLOP","VIDEO","VID","PATTERN","PAT",
                        "DURATION","DUR","TIMEOUT","TIM","RUNT","WINDOW","WIND","DELAY",
                        "DEL","SETUP","SET","NEDGE","RS232","IIC","SPI","CAN","FLEXRAY",
                        "FLEX","LIN","IIS","M1553"]:
            raise InstrumentError("Invalid trigger mode")
        self._write(":TRIG:MODE {mode}".format(mode=mode))

    def set_trigger_coup(self, coup):
        if coup not in ["AC","DC","LFREJECT","LFR","HFREJECT","HFR"]:
            raise InstrumentError("Invalid trigger coupling")
        self._write(":TRIG:COUP {coup}".format(coup=coup))

    def get_trigger_status(self):
        return self._ask(":TRIG:STAT")

    def set_trigger_sweep(self, sweep):
        if sweep not in ["AUTO","NORMAL","NORM","SINGLE","SING"]:
            raise InstrumentError("Invalid trigger sweep")
        self._write(":TRIG:SWE {sweep}".format(sweep=sweep))

    def set_trigger_source(self, source):
        if source not in ["D0","D1","D2","D3","D4","D5","D6","D7",
                          "D8","D9","D10","D11","D12","D13","D14","D15",
                          "CHANNEL1","CHAN1","CHANNEL2","CHAN2",
                          "CHANNEL3","CHAN3","CHANNEL4","CHAN4","ACLINE","ACL"]:
            raise InstrumentError("Invalid trigger source")
        self._write(":TRIG:EDGE:SOUR {source}".format(source=source))

    def set_trigger_slope(self,slope):
        if slope not in ["POSITIVE","POS","NEGATIVE","NEG","RFALI","RFAL"]:
            raise InstrumentError("Invalid trigger slope")
        self._write(":TRIG:EDGE:SLOPE {slope}".format(slope=slope))

    def set_trigger_level(self, level=0.0):
        self._write(":TRIG:EDGE:LEV {level}".format(level=level))

    def arm_trigger(self):
        pass

    def save_screendump(self, filename):
        """Save a screendump to a file. Screendump file is in .bmp format"""
        f = open(filename, "wb")
        res = self._ask_read_raw(':DISP:DATA?')
        # Split the header and data into separate arrays
        header = res[0:11]
        data = res[11:]
        # Get size from header
        size = int(header[2:])
        # Open the file to write the bitmap info into
        f = open(filename, "wb")
        # Write the bitmap info into the file
        f.write(data)
        # Set the file size to what was sent in the header
        f.truncate(size)
        # Close the file
        f.close()

    def console(self):
        self._console("RIGOL MSO5000")


