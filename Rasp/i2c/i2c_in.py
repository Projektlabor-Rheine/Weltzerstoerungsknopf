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


    async def i2_lister:
        while True:
            time.sleep(0.05)
            but_in = bus.read_byte(ADDRESS)
            but_in = but_in >> 4
            if but_in & ButMasks.BUT_UP.value > 0:
                pass
            elif but_in & ButMasks.BUT_DOWN.value > 0:
                pass
            elif but_in & ButMasks.BUT_OK.value > 0:
                pass
            elif but_in & ButMasks.BUT_CANCEL.value > 0:
                pass





