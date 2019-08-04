import sys
import os
import subprocess as sp

import readchar

import serial
import serial.tools.list_ports
from serial.threaded import ReaderThread, Protocol


class SerialProtocol(Protocol):

    ENCODING = 'utf-8'
    UNICODE_HANDLING = 'replace'

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        d = data.decode(self.ENCODING, self.UNICODE_HANDLING)
        print(d, end='')

    def connection_lost(self, exc):
        if exc:
            print(exc)

        print('\r\nport closed')

        self.transport = None

    def write_packet(self, data, is_binary=0):
        if self.transport:
            if is_binary:
                self.transport.write(data)
            else:
                self.transport.write(data.encode(self.ENCODING, self.UNICODE_HANDLING))


if __name__ == "__main__":

    if 'PYTHONUNBUFFERED' not in os.environ:

        os.environ['PYTHONUNBUFFERED'] = '1'

        print(sys.executable)
        print(sys.argv)

        command = [sys.executable]
        command.extend(sys.argv)

        sp.call(command)

        sys.exit(0)

    ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200, timeout=1)

    print(readchar.key)
    with ReaderThread(ser, SerialProtocol) as protocol:
        while True:
            key = readchar.readkey()
            if key == readchar.key.CTRL_D:
                break
            protocol.write_packet(key)
