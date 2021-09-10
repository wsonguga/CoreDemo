#!/usr/bin/env python3

import serial
import time
import serial.tools.list_ports

# ports = list(serial.tools.list_ports.comports())
# port = None
# for p in ports:
#     print(p)
#     port = p.device

port = "/dev/ttyUSB0"
print("Write:", port)

ser = serial.Serial(port, baudrate=115200, timeout=5)
ser.write(b"\xcd\x11")
# ser.write(b"cd11")
time.sleep(1)
