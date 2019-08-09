#!/usr/bin/env python3

import logging
import serial

logging.basicConfig(level=logging.DEBUG)


ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, stopbits=1, parity=serial.PARITY_ODD, bytesize=8, timeout=60)

# ser.open()

print("open success")

while ser.isOpen():

    try:
        data = ser.readline()
        data = data.decode(encoding='latin-1')
        print(data.rstrip())
    except:
        print(data)

    pass

    # '*%IR iZYy.zM W \x16y.L\tj1S-֢4ӺdS4NR*%Ij\n\x0276&S'

    # dataStr = str(base64.decodestring(base64.encodestring()))

    # data = ser.readline() #???,? \n ??,???? \n ????,??
    # data = ser.readlines() #????????
    # data = ser.xreadlines() #????????


print("not open")
