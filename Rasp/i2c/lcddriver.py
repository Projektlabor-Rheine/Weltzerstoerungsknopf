﻿import sys
sys.path.append("./lib")

import i2c_lib
from time import *
from enum import Enum
from i2c_in import Buttons
from i2c_in import Edges
from i2c_in import InObj
from terminal import i2cIn

# LCD Address
ADDRESS = 0x3f

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

#Classes
class Layer(Enum):
   Overlay = 1
   Underlay = 2

class ViewObj():

   def __init__(self, advlcd, span, layer):
      #span -> count of lines 4 or 2
      self.advlcd = advlcd
      self.layer = layer
      self.span = span
   
   def update(self):
      pass



class lcd:
   #initializes objects and lcd
   def __init__(self):
      self.lcd_device = i2c_lib.i2c_device(ADDRESS)

      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x03)
      self.lcd_write(0x02)

      self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      sleep(0.2)

   # clocks EN to latch command
   def lcd_strobe(self, data):
      self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
      sleep(.0005)
      self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
      sleep(.0001)

   def lcd_write_four_bits(self, data):
      self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
      self.lcd_strobe(data)

   # write a command to lcd
   def lcd_write(self, cmd, mode=0):
      self.lcd_write_four_bits(mode | (cmd & 0xF0))
      self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))
      
   #turn on/off the lcd backlight
   def lcd_backlight(self, state):
      if state in ("on","On","ON"):
         self.lcd_device.write_cmd(LCD_BACKLIGHT)
      elif state in ("off","Off","OFF"):
         self.lcd_device.write_cmd(LCD_NOBACKLIGHT)
      else:
         print("Unknown State!")

   # put string function
   def lcd_display_string(self, string, line):
      if line == 1:
         self.lcd_write(0x80)
      if line == 2:
         self.lcd_write(0xC0)
      #unnessecary 
      if line == 3:
         self.lcd_write(0x94)
      if line == 4:
         self.lcd_write(0xD4)

      for char in string:
         self.lcd_write(ord(char), Rs)

   # clear lcd and set to home
   def lcd_clear(self):
      self.lcd_write(LCD_CLEARDISPLAY)
      self.lcd_write(LCD_RETURNHOME)


class LcdAdv(lcd):

   overlay_visible = True
   underlay = ["", "", "", ""]
   overlay = ["", "", "", ""]

   def lcd_display_string(self, string, line, layer = Layer.Underlay):
      if layer == Layer.Underlay:
         self.underlay[line] = string
      elif layer == Layer.Overlay:
         self.overlay[line] = string

      if line == 1:
         self.lcd_write(0x80)
      if line == 2:
         self.lcd_write(0xC0)
      if line == 3:
         self.lcd_write(0x94)
      if line == 4:
         self.lcd_write(0xD4)

      for char in string:
         if self.overlay_visible and layer == Layer.Overlay:
            if string != "":
               self.lcd_write(ord(char), Rs)
            else:
               self.lcd_write(ord(char), Rs)
         elif not(self.overlay_visible) and layer == Layer.Underlay:
               self.lcd_write(ord(char), Rs)

   def set_overlay_visible(self, visible = False):
      self.overlay_visible = visible
      self.update()

   def update(self):
      for i in range(0, 4):
         self.lcd_display_string(self.overlay[i], i, Layer.Overlay)
      for i in range(0, 4):
         self.lcd_display_string(self.underlay[i], i, Layer.Underlay)



class ScrollList(ViewObj, InObj):

   selection = 0
   scroll = 0

   #Perhaps insert init here

   def inEvent(self, button, edge, focus):
      if focus == False:
         return
      if button == Buttons.UP and edge == Edges.RISING:
         if self.selection > 0:
            self.selection-=1
            if self.scroll == self.selection:
               self.scroll-=1
         self.update()
      elif button == Buttons.DOWN and edge == Edges.RISING:
         if self.selection < len(self.items)-1:
            self.selection+=1
            if self.scroll+self.span == self.selection:
               self.scroll+=1
         self.update()
      elif button == Buttons.OK and edge == Edges.RISING:
         self.items[self.selection].functio()

   def set_items(self, items):
      self.items = items
      self.update()


   def update(self):
      for i in range(0, self.span):
         if i+self.scroll == self.selection:
            self.advlcd.lcd_display_string("[" + self.items[i+self.scroll].title[:14] + "]", i, Layer.Underlay)
         else:
            self.advlcd.lcd_display_string(" " + self.items[i+self.scroll].title[:14] + " ", i, Layer.Underlay)
      

      


class ListItem:

   def __init__(self, title, functio):
      self.title = title
      self.functio = functio





class YNMenu(ViewObj, InObj):
   
   # 0 = yes | 1 = no
   selection = 0
   yes = "yes"
   no = "no"
   novisible = True
   todisplay = ""

   def __init__(self, advlcd, okable, yescall, nocall=None, stopcall=None, label=""):
      if label == "":
         super.__init__(advlcd, 1, Layer.Overlay)
      else:
         super.__init__(advlcd, 2, Layer.Overlay)
      self.label = label
      self.okable = okable
      self.yescall = yescall
      self.nocall = nocall
      self.stopcall = stopcall
      i2cIn.add_to_lister(self)

   def show(self):
      self.todisplay = "[" + self.yes + "]"
      if self.novisible:
         self.todisplay = self.todisplay + self.no + " "
      self.todisplay = "                "[:16-len(self.todisplay)]+self.todisplay
      self.update()
      i2cIn.getFocus(self)

   def change_selection(self):
      if self.selection == 0 and self.novisible:
         self.todisplay = "[" + self.yes + "]" + self.no + " "
         self.todisplay = "                "[:16-len(self.todisplay)]+self.todisplay
         self.update()
         self.selection = 1
      elif self.selection == 1 and self.novisible:
         self.todisplay = " " + self.yes + "[" + self.no + "]"
         self.todisplay = "                "[:16-len(self.todisplay)]+self.todisplay
         self.update()
         self.selection = 0

   def hide(self):
      self.todisplay = ""
      update()
      self.advlcd.set_overlay_visible(False)
      i2cIn.remFocus(self)


   def update(self):
      if span == 2:
         self.advlcd.lcd_display_string(self.label, 1, self.layer)
      self.advlcd.lcd_display_string(self.todisplay, 2, self.layer)


   def inEvent(self, button, edge, focus):
      if focus == False:
         return
      if button == Buttons.OK:
         if self.selection == 0:
            if edge == Edges.RISING:
               self.yescall(button)
            elif self.okable == False and edge == Edges.FALLING and self.stopcall != None:
               self.stopcall(button)
            if self.okable == True:
               self.hide()
         else:
            if self.nocall != None:
               self.hide()
               self.nocall()
      elif (button == Buttons.UP or button == Buttons.DOWN) and edge == Edges.RISING:
         self.change_selection()
      elif button == Buttons.CANCEL and edge == Edges.RISING:
         self.hide()

   def setyesno(self, yes, no, novisible = True):
      self.yes = yes
      self.no = no
      self.novisible = novisible


      



