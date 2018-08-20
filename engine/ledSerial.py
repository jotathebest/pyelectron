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
        elif sys.platform.startswith(
                'linux') or sys.platform.startswith('cygwin'):
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

    def init_arduino(self, *args, **kwargs):
        '''
        Initializes a communication port with Arduino
        '''

        baudrate = kwargs.get("baudrate", self.baudrate)
        bytesize = kwargs.get("bytesize", self.bytesize)
        parity = kwargs.get("parity", self.parity)
        stopbits = kwargs.get("stopbits", self.stopbits)
        timeout = kwargs.get("timeout", self.timeout)
        xonxoff = kwargs.get("xonxoff", self.xonxoff)
        rtscts = kwargs.get("rtscts", self.rtscts)
        dsrdtr = kwargs.get("dsrdtr", self.dsrdtr)
        serial_port_path = kwargs.get("serial_port_path", None)

        if serial_port_path is None:
            raise("[ERROR] You must define a serial port path")

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


def main(arduino=ArduinoSerial()):
    # Searchs for available ports
    if len(arduino.available_ports) == 0:
        arduino.search_serial_ports()
    kwargs = {}

    for port in arduino.available_ports:
        print("[INFO] Sending message to port {}".format(port))
        kwargs["serial_port_path"] = port
        arduino.init_arduino(**kwargs)
        arduino.turn_on_led()
        time.sleep(2)
        arduino.turn_off_led()
        time.sleep(2)


if __name__ == '__main__':
    arduino = ArduinoSerial()
    while True:
        main(arduino=arduino)
