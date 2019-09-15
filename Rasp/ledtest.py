#!/usr/bin/python

import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D21, 30, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

pixels.fill((255, 0, 0))

pixels.show()


time.sleep(3)


