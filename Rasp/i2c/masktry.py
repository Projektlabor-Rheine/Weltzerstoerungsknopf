#!/usr/bin/python
import time
import smbus
from enum import Enum

ADDRESS = 0x38
bus = smbus.SMBus(1)

print(bin(bus.read_byte(ADDRESS)))

class ButMasks(Enum):
    BUT_UP = 0b0001
    BUT_DOWN = 0b0010
    BUT_OK = 0b0100
    BUT_CANCEL = 0b1000




class i2cin:

    def i2_lister(self, but_in):
        time.sleep(0.05)
        but_in = but_in >> 4
        if but_in & ButMasks.BUT_UP.value > 0:
            print("up")
            pass
        if but_in & ButMasks.BUT_DOWN.value > 0:
            print("down")
            pass
        if but_in & ButMasks.BUT_OK.value > 0:
            print("ok")
            pass
        if but_in & ButMasks.BUT_CANCEL.value > 0:
            print("cancel")
            pass


inp = i2cin()

#Theese are the major types of inputs 
inp.i2_lister(0b00011111)
inp.i2_lister(0b00101111)
inp.i2_lister(0b01001111)
inp.i2_lister(0b10001111)

#WORKS NICELY

#And with multiple flags set
inp.i2_lister(0b10101111)

while True:
    time.sleep(0.05)
    inp.i2_lister(bus.read_byte(ADDRESS))




