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

class Edges(Enum):
    RISING = 1
    FALLING = 2

class Buttons(Enum):
    OK = 1
    UP = 2
    DOWN = 3
    CANCEL = 4

class InObj():

    def inEvent(self, button, edge, focus):
        pass


class i2cin:

    lister = []
    focus = []
    lock = [False, False, False, False]
    #Buttons: UP, DOWN, OK, CANCEL
    but_state = 0
    
    def add_to_lister(self, in_obj : InObj):
        self.lister.append(in_obj)

    async def i2_lister(self):
        while True:
            time.sleep(0.05)
            # but_in represents the button state in binary
            but_in = bus.read_byte(ADDRESS)
            but_in = but_in >> 4
            # dif_but_in represents the buttons that have changed in binary
            dif_but_in = self.but_state ^ but_in
            if dif_but_in & ButMasks.BUT_UP.value > 0: 
                for i in range(0, len(self.lister)):
                    self.lister[i].inEvent(Buttons.UP, Edges.RISING if (but_in & ButMasks.BUT_UP.value > 0) else Edges.FALLING, True if i == self.focus[len(self.focus)-1] else False)
                time.sleep(0.15)
            if dif_but_in & ButMasks.BUT_DOWN.value > 0:
                for i in range(0, len(self.lister)):
                    self.lister[i].inEvent(Buttons.DOWN, Edges.RISING if (but_in & ButMasks.BUT_DOWN.value > 0) else Edges.FALLING, True if i == self.focus[len(self.focus)-1] else False)
                time.sleep(0.15)
            if dif_but_in & ButMasks.BUT_OK.value > 0:
                for i in range(0, len(self.lister)):
                    self.lister[i].inEvent(Buttons.OK, Edges.RISING if (but_in & ButMasks.BUT_OK.value > 0) else Edges.FALLING, True if i == self.focus[len(self.focus)-1] else False)
                time.sleep(0.15)
            if dif_but_in & ButMasks.BUT_CANCEL.value > 0:
                for i in range(0, len(self.lister)):
                    self.lister[i].inEvent(Buttons.CANCEL, Edges.RISING if (but_in & ButMasks.BUT_CANCEL.value > 0) else Edges.FALLING, True if i == self.focus[len(self.focus)-1] else False)
                time.sleep(0.15)
            #set for next iteration
            self.but_state = but_in

    def getFocus(self, in_obj : InObj):
        focus = 0
        try:
            focus = self.lister.index(in_obj)
        except ValueError:
            print("Add to inObj to lister first")
            return
        try:
            isalready = self.focus.index(focus)
            self.focus.pop(isalready)
            self.focus.append(focus)
        except ValueError:
            self.focus.append(focus)
            

    def remFocus(self, in_obj : InObj):
        focus = self.lister.index(in_obj)
        if focus > -1:
            self.focus.remove(focus)
            

    







