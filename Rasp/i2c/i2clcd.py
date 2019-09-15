import lcddriver
import time

lcd = lcddriver.lcd()
lcd.lcd_clear()

lcd.lcd_display_string("Projektlabor", 1)
lcd.lcd_display_string("   Projektlabor!", 2)
