#!/usr/bin/python
import time
import smbus


bus = smbus.SMBus(1)
ADDRESS = 0x38
print(bin(bus.read_byte(ADDRESS)))
