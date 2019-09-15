#!/usr/bin/python

from escpos.printer import Usb

p = Usb(0x0416, 0x5011)
p.text("\n\n\n\n\nBitte nicht fuettern\n\n\n\n\n")
p.cut()

