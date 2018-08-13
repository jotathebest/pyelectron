import sys
import glob
import serial
import time


class ArduinoSerial:

    def __init__(self, *args, **kwargs):
        self.available_ports = []
        self.baudrate = kwargs.get('baudrate', 115200)
        self.bytesize = kwargs.get('bytesize', 8)
        self.parity = kwargs.get('parity', 'N')
        self.stopbits = kwargs.get("stopbits", 1)
        self.timeout = kwargs.get('timeout', None)
        self.xonxoff = kwargs.get('xonxoff', False)
        self.rtscts = kwargs.get('rtscts', False)
        self.dsrdtr = kwargs.get('dsrdtr', False)

    def search_serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        self.available_ports = result

    def init_arduino(self, serial_port_path,
                     baudrate=None,
                     bytesize=None,
                     parity=None,
                     stopbits=None,
                     timeout=None,
                     xonxoff=None,
                     rtscts=None,
                     dsrdtr=None):
        '''
        Initializes a communication port with Arduino
        '''
        if baudrate is None:
            baudrate = self.baudrate
        if bytesize is None:
            bytesize = self.bytesize
        if parity is None:
            parity = self.parity
        if stopbits is None:
            stopbits = self.stopbits
        if timeout is None:
            timeout = self.timeout
        if xonxoff is None:
            xonxoff = self.xonxoff
        if rtscts is None:
            rtscts = self.rtscts
        if dsrdtr is None:
            dsrdtr = self.dsrdtr

        self.arduino = serial.Serial(port=serial_port_path,
                                     baudrate=baudrate,
                                     bytesize=bytesize,
                                     parity=parity,
                                     stopbits=stopbits,
                                     timeout=timeout,
                                     xonxoff=xonxoff,
                                     rtscts=rtscts,
                                     dsrdtr=dsrdtr)

    def turn_on_led(self):
        self.arduino.write(b"on")

    def turn_off_led(self):
        self.arduino.write(b"off")


def main():
    arduino = ArduinoSerial()
    arduino.search_serial_ports()

    for port in arduino.available_ports:
        print("[INFO] Sending message to port {}".format(port))
        arduino.init_arduino(port)
        arduino.turn_on_led()
        time.sleep(2)
        arduino.turn_off_led()
        time.sleep(2)


if __name__ == '__main__':
    main()
