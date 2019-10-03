#!/usr/bin/python
import time
import smbus
from enum import Enum
from terminal import Buttons



ADDRESS = 0x38
bus = smbus.SMBus(1)


print(bin(bus.read_byte(ADDRESS)))


class ButMasks(Enum):
    BUT_UP = 0b0001
    BUT_DOWN = 0b0010
    BUT_OK = 0b0100
    BUT_CANCEL = 0b1000

class Edges(Enum):
    RISING = 1
    FALLING = 2

class Buttons(Enum):
    OK = 1
    UP = 2
    DOWN = 3
    CANCEL = 4

class InObj():

    def inEvent(self, button, edge):
        pass


class i2cin:

    lister = []
    focus = 0
    
    def add_to_lister(self, in_obj):
        self.lister.append(in_obj)

    async def i2_lister(self):
        while True:
            time.sleep(0.05)
            but_in = bus.read_byte(ADDRESS)
            but_in = but_in >> 4
            if but_in & ButMasks.BUT_UP.value > 0:
                for lister in self.lister:
                    lister.inEvent(Buttons.UP)
            if but_in & ButMasks.BUT_DOWN.value > 0:
                for lister in self.lister:
                    lister.inEvent(Buttons.DOWN)
            if but_in & ButMasks.BUT_OK.value > 0:
                for lister in self.lister:
                    lister.inEvent(Buttons.OK)
            if but_in & ButMasks.BUT_CANCEL.value > 0:
                for lister in self.lister:
                    lister.inEvent(Buttons.CANCEL)

    def getFocus(self, in_obj):
        focus = lister.index(in_obj)
        if focus < 0:
            focus = 0







