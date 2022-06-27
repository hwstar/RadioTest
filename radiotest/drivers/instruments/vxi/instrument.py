import time
import vxi11
import vxiinstrclasses.__version__ as pkgvers

#
# This is an error class used by all of the instrument modules to throw an exception
#

class InstrumentError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

#
# This is a base class to be used by all of the specific instrument classes
#


class Instrument:
    def __init__(self, resourcehost):
        self.s = vxi11.Instrument(resourcehost)
        self._debug_flag=False

    def debug(self, state):
        """Print debug messages to console"""
        self._debug_flag = state

    def _debug_print(self, message, action=''):
        """Print a debug message"""
        print('Debug: '+ action + ' ',end='')
        print(message)

    def _write(self, message):
        """Send a message to an instrument"""
        if self._debug_flag:
            self._debug_print(message, 'Writing:')
        self.s.write(message)

    def write(self, message):
        """Send a message to an instrument"""
        self._write(message)

    def _write_raw(self, message):
        """Send a binary message to an instrument"""
        if self._debug_flag:
            self._debug_print(message, 'Writing raw:')
        self.s.write_raw(message)

    def _read_raw(self, num=-1):
        """Read a binary response from an instrument"""
        return self.s.read_raw(num)

    def _ask(self, message):
        """Send a command and wait for a response"""
        if self._debug_flag:
            self._debug_print(message, 'Asking:')
        res = self.s.ask(message)
        if self._debug_flag:
            self._debug_print(res, 'Ask return:')
        return res

    def ask(self, message):
        """Send a command and wait for a response"""
        return self._ask(message)

    def _ask_read_raw(self, message, length=-1):
        """Send a command and wait for a binary response"""
        self._write(message)
        res = self.s.read_raw(length)
        if self._debug_flag:
            self._debug_print(res, 'Ask read raw return:')
        return res

    def ask_read_raw(self, message, length=-1):
        """Send a command and wait for a binary response"""
        return self._ask_read_raw(message, length)

    def _console(self, ident):
        """Debugging aid: opens a console to send commands. See the commands in the user manual"""
        cmd = ''
        while cmd != 'exit()':
            cmd = input(ident+' console, Type exit() to leave> ')
            if cmd.find('?') >= 0:
                answer = self.s.ask(cmd)
                print(answer)
            elif cmd.find('?') < 0 and cmd != 'exit()':
                self.s.write(cmd)
        else:
            print('Exiting the '+ident+' console')

    def reset(self):
        """resets the instrument, registers,buffers"""
        self._write("*RST")
        time.sleep(0.2)

    def wait(self):
        """waits for the previous command to complete"""
        self._write("*WAI")
        time.sleep(0.2)

    def identify(self):
        """Return instrument identity information"""
        return self.s.ask("*IDN?")

    def close(self):
        """Close the connection to the instrument"""
        self.s.close()



