#!/usr/bin/python

from ABE_ExpanderPi import IO
from ABE_helpers import ABEHelpers
import time

"""
================================================
ABElectronics Expander Pi | Digital I/O Interrupts Demo
Version 1.0 Created 21/08/2014

Requires python smbus to be installed with: sudo apt-get install python-smbus
run with: sudo python demo-iowrite.py
================================================

This example uses the write_pin and writeBank methods to switch the pins
on and off on the I/O bus.

Initialise the IO class and create an instance called io.
"""



class HDLX2416:

    """
    Based on Agilent HDLX-2416
    """

    # Define PINS of the 2416
    # Data bus
    DATA_BUS = 0

    #CRTL BUS
    CTRL_BUS = 1 # ctrl pins are at bus 1
    WR = 1 << 2
    CU = 1 << 3
    CE = 1 << 4
    LED = 1 << 5
    A0 = 1 << 6
    A1 = 1 << 7
    EFD = 1 << 6
    CTRL_IDLE = WR + CE + LED

    def __init__(self, io):
        # We will write to the pins 1 to 16 so set port 0&1 to be outputs and turn all off
        # the pins
        self._io = io
        self._io.set_port_direction(0, 0x00)
        self._io.set_port_direction(1, 0x00)
        self._io.write_port(self.DATA_BUS, 0x00)
        self._io.write_port(self.CTRL_BUS, self.CTRL_IDLE)
        return

    # public methods
    def set_chr(self, character, position):

        #display character at position
        # write character to bus
        self._io.write_port(self.DATA_BUS, character)

        # take over data, set address and
        position = 3 - position
        ctrl = self.CU + (position << 6)
        self._io.write_port(self.CTRL_BUS, ctrl)
        self._io.write_port(self.CTRL_BUS, self.CTRL_IDLE)
        return

    def set_brightness(self, value):
        # set display brightness
        # value can be from 0 (100%) to 7 (3%)

        data = (value << 3)
        self._io.write_port(self.DATA_BUS, data)
        ctrl = 0
        self._io.write_port(self.CTRL_BUS, ctrl)
        self._io.write_port(self.CTRL_BUS, self.CTRL_IDLE)

    def display_text(self, text, speed):
        # display text a moving text
        # speed is the moving speed

        if (len(text) < 5):
            index = 0
            while (index < len(text)):
                self.set_chr(ord(text[index]), index)
                index += 1
        else:
            # fill display with first 3 characters from left to right
            start = 3
            while (start >= 0):
                x = start
                index = 0
                while (x < 4):
                    self.set_chr(ord(text[index]), x)
                    x += 1
                    index += 1
                start -= 1
                time.sleep(speed)

            # now the row is filled, we write from left to right
            start = 1
            while (len(text) - start >= 4):
                x = 0
                index = start
                while (x < 4):
                    self.set_chr(ord(text[index]), x)
                    x += 1
                    index += 1
                start += 1
                time.sleep(speed)


i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
io = IO(bus)

hdlx = HDLX2416(io)

hdlx.display_text ("    ", 0)
time.sleep(0.5)
hdlx.display_text ("Volker", 0.2)
time.sleep(0.5)
hdlx.display_text ("Lina Moesker", 0.2)
