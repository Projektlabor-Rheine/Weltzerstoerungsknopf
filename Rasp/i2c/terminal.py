from enum import Enum
#import lcddriver
from multiprocessing.connection import Listener
from multiprocessing.context import AuthenticationError
import asyncio
import json
import i2c_in
import lcddriver
import time
import queue


######## CONFIG #########

BUT_ADDR = 0x38
LCD_ADDR = 0x3f

######## END CONFIG ########

class shrtNamePin(Enum):
    #Shutdown
    #IO14 is already handled
    SHTDWN = 15
    #schere
    SCHM1 = 26
    SCHM2 = 13
    SCHE1 = 19
    SCHE2 = 6
    #Perry
    RTKNPF = 17
    HNDNDSCHLTR = 27
    RTSCHLTR = 5
    NEBEL = 16
    #Hand
    EN = 11
    INA = 10
    INB = 9 
    #LED
    LEDR = 22
    LEDS1 = 21
    LEDS2 = 20
    #LED Schritte
    WLTSCHRFT = 12
    STEP1 = 23
    STEP2 = 8
    STEP3 = 25

#Commands / Transmit
#Restart
#hand move params: FORWARD STOP BACKWARD
#schere move params: FORWARD STOP BACKWARD
#change output of gpio pin params: channel, out
#get input of gpio pin params: channel recive: in
#printer test
#light test
#led strip test
#hand test
#schere test
#nebel test params: START STOP
class Commands(Enum):
    Restart = 1
    MoveHand = 2
    MoveSchere = 3
    GPIOOut = 4
    GPIOIn = 5
    PrinterTest = 6
    LightTest = 7
    LEDTest = 8
    HandTest = 9
    SchereTest = 10
    NebelTest = 11

#Events / Recive
#Interrupt on channel params: channel, edge
#program phase changed params: before, after
#Exception raised params: Exception
#Timeout on channel params: channel
#shutdown
class Events(Enum):
    Interrupt = 1
    PhaseChange = 2
    Exceptio = 3
    Timeout = 4
    Shutdown = 5

def json_interpret(msgstr = '{"2":[2,3,"leeil"]}'):
    jsonobj = json.loads(msgstr)
    for item in jsonobj:
        return (Events(int(item)), jsonobj[item])
    
# Json string to transmit: "number of command":[Array of Arguments]
# Json string to recieve: "number of event":[Array of Arguments]
# e.g. {"4":[2,"test"]} | {} required
async def sock_task():
    while True:
        #read msg
        msg = conn.recv()   
        # do something with msg
        print(repr(msg))
        #interpret msg
        evcom, args = json_interpret(msg)
        print(str(evcom.name) + " " + str(evcom.value))
        for item in args:
            print(item)
        if evcom == Events.Shutdown:
            #shutdown soon
            conn.close()
            break
    listener.close()


async def main():
    socktask = asyncio.create_task(sock_task())
    buttask = asyncio.create_task(i2cIn.i2_lister())
    await socktask
    await buttask

###### METHODS END ########

###### PRE BEGIN #######

#I2C input
i2cIn = i2c_in.i2cin()
#LCD
lcd = lcddriver.LcdAdv(i2cIn)
#Socket communication
address = ('localhost', 21122)
listener = Listener(address, authkey=b'Welti')
#Fifo buffer
fifo = queue.Queue()

def yncall(command, comargs):
    print("yncall")
    if isinstance(command, Commands):
        print("add to fifo " + str(command.name))

def scroll_item_eve(label, command, comargs=0):
    menu = lcddriver.YNMenu(lcd, True, yncall, yescallargs=(command, comargs), label=label)
    menu.show()


###### PRE BEGIN END ######

###### BEGIN ######

#starting the main Welti program

print("Waiting for connection...")
lcd.lcd_display_string("Waiting for connection...", 1, lcddriver.Layer.Overlay)
conn = 0
while True:
    try:
        conn = listener.accept()
        break
    except AuthenticationError:
        print("digest reveived was wrong")
        print("tring again")
print( 'connection established from', listener.last_accepted )
lcd.lcd_display_string("connection established from " + str(listener.last_accepted), 1, lcddriver.Layer.Overlay)
time.sleep(1)
lcd.lcd_clear()

#Scrolllist
sclist = lcddriver.ScrollList(lcd, 2, lcddriver.Layer.Underlay)
sclist.add_item(lcddriver.ListItem("Eventlog", None))
sclist.add_item(lcddriver.ListItem("Handtest", scroll_item_eve, functionargs=("Start LEDtest", Commands.HandTest)))
sclist.add_item(lcddriver.ListItem("Scherentest", scroll_item_eve, functionargs=("Strt Scherentest", Commands.SchereTest)))
sclist.add_item(lcddriver.ListItem("Printertest", scroll_item_eve, functionargs=("Strt Printertest", Commands.PrinterTest)))
sclist.add_item(lcddriver.ListItem("Lighttest", None))
sclist.add_item(lcddriver.ListItem("LED-Striptest", scroll_item_eve, functionargs=("Start LEDtest", Commands.LEDTest)))
sclist.add_item(lcddriver.ListItem("Nebeltest", scroll_item_eve, functionargs=("Start Nebeltest", Commands.NebelTest)))
sclist.add_item(lcddriver.ListItem("Restart", scroll_item_eve, functionargs=("Sure to Restart?", Commands.Restart)))



asyncio.run(main())

####### END #######
