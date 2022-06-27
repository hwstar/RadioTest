import time
import math
import struct
from .instrument import Instrument, InstrumentError



class Sdg1032x(Instrument):
    """This class controls a Siglent 1032X arbitrary waveform generator"""

    def rst(self):
        self._write("*RST")
        self.output_off(2)
        self.output_off(1)

    def __init__(self, resourcehost):

        Instrument.__init__(self, resourcehost)

        self.iid = self.identify()
        if (self.iid[0:29] != 'Siglent Technologies,SDG1032X'):
            raise InstrumentError('Instrument Manufacturer/Model Number Mismatch,  '+self.iid)
        self.make, self.model, self.sn, self.fw = [self.iid.split(",")[i] for i in range(0, 4)]

        self.rst()

    def console(self):
        """Enter debugging console"""
        self._console("Siglent SDG1032X")

    def output(self, param, channel=1):
        """Set output parameters"""
        cstr = "C{channel}:OUTP {param} ".format(channel=channel, param=param)
        self._write(cstr)

    def output_on(self, channel=1):
        """Turn output on"""
        self.output('ON', channel=channel)

    def output_off(self, channel=1):
        """Turn output off"""
        self.output('OFF', channel=channel)

    def output_sourcez(self, channel=1, load=50000):
        """Set output source impedance"""
        lstr="LOAD, {load}".format(load=load)
        self.output("{lstr}".format(lstr=lstr), channel)

    def output_polarity_normal(self, channel=1):
        """Set output polarity to normal"""
        self.output("PLRT, NOR", channel)

    def output_set_defaults(self, channel=1):
        """Set the output defaults"""
        self.output("OFF, LOAD, HZ, PLRT, NOR", channel)

    def output_polarity_invert(self, channel=1):
        """Set output polarity to inverted"""
        self.output("PLRT, INVT", channel)

    def basic_wave(self, type, channel=1, freq=1000, amplitude=1.0, offset=0.0, phase=0.0, sym=float('nan'), duty=float('nan')):
        """Output a basic waveform"""
        if(math.isnan(sym) == False):
            self._write(
                "C{channel}:BSWV WVTP, {type},FRQ, {freq}HZ,AMP, {amplitude}V,OFST, {offset}V,PHSE, {phase},SYM, {sym}".format(
                    channel=channel, type=type, freq=freq, amplitude=amplitude, offset=offset, phase=phase, sym=sym))
        elif (math.isnan(duty) == False):
            self._write(
                "C{channel}:BSWV WVTP, {type},FRQ, {freq}HZ,AMP, {amplitude}V,OFST, {offset}V,PHSE, {phase},DUTY, {duty}".format(
                    channel=channel, type=type, freq=freq, amplitude=amplitude, offset=offset, phase=phase, duty=duty))

        else:
            self._write(
                "C{channel}:BSWV WVTP, {type},FRQ, {freq}HZ,AMP, {amplitude}V,OFST, {offset}V,PHSE, {phase}".format(
                    channel=channel, type=type, freq=freq, amplitude=amplitude, offset=offset, phase=phase))


    def sine(self, channel=1, freq=1000, amplitude=1.0, offset=0.0, phase=0.0):
        """Output a sine wave"""
        self.basic_wave(type="SINE",channel=channel, freq=freq, amplitude=amplitude, offset=offset, phase=phase)

    def ramp(self, channel=1, freq=1000, amplitude=1.0, offset=0.0, phase=0.0, sym=50):
        """Output a ramp wave"""
        self.basic_wave(type="RAMP", channel=channel, freq=freq, amplitude=amplitude, offset=offset, phase=phase, sym=sym)

    def square(self, channel=1, freq=1000, amplitude=1.0, offset=0.0, phase=0.0, duty=50):
        """Output a square wave"""
        self.basic_wave(type="SQUARE", channel=channel, freq=freq, amplitude=amplitude, offset=offset, phase=phase, duty=duty)

    def noise(self, channel=1, stdev=0.200, mean=0):
        """Output noise"""
        self._write("C{channel}:BSWV WVTP,NOISE,STDEV,{stdev}V,MEAN,{mean}V".format(channel=channel, stdev=stdev, mean=mean))

    def sweep_off(self, channel):
        """Turn sweep mode off"""
        self._write("C{channel}:SWWV STATE,OFF")

    def sinesweep(self, channel=1, time=1.0, amplitude=1.0, mode="LIN", start=300.0, stop=3000.0):
        """Basic sine sweep"""
        sstr="C{channel}:SWWV STATE,ON,TYPE,SINE,".format(channel=channel)
        sstr=sstr+"TIME,{time}S,AMP,MODE,{mode},START,{start}HZ,STOP,{stop}HZ".format(time=time, mode=mode, start=start, stop=stop)
        self._write(sstr)

    def wave_select_by_name(self, name, channel=1):
        """Select an user waveform by name"""
        sstr = "C{channel}:ARWV NAME,{name}".format(channel=channel, name=name)
        self._write(sstr)

    def wave_select_by_index(self, index, channel=1):
        """Select builtin arbitrary wave by index"""
        sstr = "C{channel}:ARWV INDEX,{index}".format(channel=channel, index=index)
        self._write(sstr)


    def wave_get_builtin(self):
        """Return a dict with built-in wave names and indexes"""
        sstr = "STL? BUILDIN"
        res = self._ask(sstr)
        res = res[4:]
        res = res.replace(' ', '')
        alist = res.split(',')
        alistlen = len(alist)
        # Get rid of leading 'M'on index
        for i in range(alistlen):
            if i % 2 == 0:
                alist[i] = int(alist[i][1:])
        # Convert the list to a dictionary
        return dict(zip(alist[1::2], alist[::2]))



    def wave_set(self, setup, channel=1):
        """Send a waveform setup to the arbitrary waveform generator
        Pass in a dict with the following items
        NAME: Name of user waveform e.g. 'test' (mandatory)
        WAVEDATA: List of signed short integers (mandatory)
        FREQ: frequency in hz (optional, default = 1000)
        TYPE: waveform type (optional, default = 5)"""

        # Mandatory parameters
        if type(setup) is not dict or 'WAVEDATA' not in setup or 'NAME' not in setup:
            return

        # Optional parameters

        if 'TYPE' not in setup:
            setup['TYPE'] = 5

        if 'FREQ' not in setup:
            setup['FREQ'] = 1000

        #Convert wave data to bytearray
        wavedata = setup['WAVEDATA']
        wdlen = len(wavedata)
        block = bytearray(wdlen*2)
        for i in range(wdlen):
            struct.pack_into('<h', block, i*2, wavedata[i])

        # assemble the block to send to the generator
        length=int(len(setup['WAVEDATA'])*2)
        #print(channel)
        wsstr = 'C{ch}:WVDT WVNM,{name},TYPE,{type},LENGTH,{length}B,FREQ,{freq},WAVEDATA,'.\
            format(ch=channel, name=setup['NAME'], type=setup['TYPE'], length=length, freq=setup['FREQ'])
        bwsstr = bytearray(wsstr.encode('utf-8'))
        block = bwsstr + block
        #print(bwsstr)
        # Send the command
        self._write_raw(block)

    def wave_get(self, memory_id='M2'):
        """Retrieve a waveform setup from the arbitrary waveform generator"""
        #Send the command
        wgstr = 'WVDT? '+ memory_id
        # Get the response
        res = self._ask_read_raw(wgstr)
        #print(res)
        # Find the binary data demarcation
        binary_data_index = res.find(b'WAVEDATA')
        # Extract the attributes and convert to utf-8
        attributes = res[5:binary_data_index - 2].decode('utf-8')
        # Strip all spaces
        attributes = attributes.replace(' ','')
        # Put the attributes in a list
        alist = attributes.split(',')
        # Convert the list to a dictionary
        adict = dict(zip(alist[::2], alist[1::2]))
        # Separate the returned binary data
        binary_data = res[binary_data_index + 9:]
        # Get rid of the newline on the end of the returned data
        binary_data = binary_data[:-1]
        # Calculate the number of short ints to unpack
        short_count = int(len(binary_data)/2)
        # if something was returned, convert the return from bytes to short integers
        if(len(adict)):
            # Convert returned length to short integer length
            if 'LENGTH' in adict:
                adict['LENGTH'] = short_count
            # Convert type from string to int
            if 'TYPE' in adict:
                adict['TYPE'] = int(adict['TYPE'])
            if 'WVNM' in adict: # Rename WVNM to name, and delete POS
                name = adict['WVNM']
                adict.pop('POS', None)
                adict.pop('WVNM', None)
                adict['NAME']=name

            wavedata = []
            #Unpack the short integers
            for i in range(short_count):
                #Generate index
                short_index = int(i*2)
                # Retrive the short integer
                word = binary_data[short_index:short_index+2]
                # Append it to the short integer array
                wavedata.append(struct.unpack('<h', word)[0])
            #print(wavedata)
            # Add the array of short integers to the return dictionary
            adict['WAVEDATA'] = wavedata
        return adict

    def channel_combine(self, ena_dis=True, channel=1):
        """Combine waveforms"""
        state = 'ON' if ena_dis is True else 'OFF'
        sstr = 'C{}:CoMBiNe {}'.format(channel, state)
        self._write(sstr)





if __name__ == "__main__":

    arb = sdg1032x("sdg1032x")
    #arb.debug(True)

    arb.output_set_defaults(1)
    arb.output_set_defaults(2)
    #arb.sine(amplitude=2, offset=0)
    #arb.sinesweep(1, time=1, start=200, stop=3500)
    #arb.noise(stdev=2.0)
    #arb.output_on()
    #arb.console()
    #print(arb.wave_get('M55'))
    setup=dict()
    setup['NAME'] = 'wave1'
    points = 16384
    wavedata = [int(0)]*points
    for i in range(points):
        m = (i*360)/points
        wavedata[i] = int(32767*math.sin(math.radians(m)))

    setup['WAVEDATA'] = wavedata
    setup['FREQ'] = 10000
    arb.wave_set(setup)
    arb.wave_select_by_index('16')
    arb.output_on()
    #print(arb.wave_get('USER,wave1'))
    print(arb.wave_get_builtin())




    arb.close()