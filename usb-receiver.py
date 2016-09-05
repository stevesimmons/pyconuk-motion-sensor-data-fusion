"""
usb-receiver.py

This is sample code from Stephen Simmons' PyCon UK 2016 talk
"Where am? What am I doing? Motion Sensor Data Fusion with Python".

It receives serial data from a microbit connected to a USB port and
prints it to stdout. From here it can be redirected to a text file, etc.

Usage:              [so far, only tested under Linux]
  $ python usb-receiver.py
  Time,AccX,AccY,AccZ,MagX,MagY,MagZ,Heading,Gesture
  630894,-144,-144,-992,5025,2712,38849,255,face up
  630948,-160,-112,-912,3725,1612,38049,254,face up
  ...

or redirecting to a file:
  $ python usb-receiver.py > data.csv

The accompanying script microbit-logger.py runs on the microbit.

Stephen Simmons - 5 Sep 2016
https://github.com/stevesimmons/pyconuk-motion-sensor-data-fusion
"""

import serial
import serial.tools.list_ports
import sys


def main():
    port = find_microbit()
    print_from_usb(port)


def find_microbit(serial_number=None):
    "Name of the first matching micro:bit's serial port, otherwise None."
    for port in serial.tools.list_ports.comports():
        if port.product == 'MBED CMSIS-DAP':
            if serial_number is None or serial_number == port.serial_number:
                return port.device
    return None


def print_from_usb(port, out=sys.stdout):
    "Write serial data from USB port to a file, by default sys.stdout."
    ser = serial.Serial(port, baudrate=115200)
    try:
        while True:
            line = ser.readline().decode()
            out.write(line)
    except:
        pass
    finally:
        ser.close()


if __name__ == '__main__':
    main()
