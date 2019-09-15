from enum import Enum

BUT_ADDR = 0x38
LCD_ADDR = 0x3f





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







