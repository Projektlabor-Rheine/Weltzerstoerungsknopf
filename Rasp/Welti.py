#!/usr/bin/python


#DDDASSSS Selbstzerstörungsskript

import RPi.GPIO as GPIO
import time
import os.path
import os
import asyncio


#CONST
#Shutdown
#IO14 is already handled
SHTDWN = 15
#schere
SCHM1 = 24
SCHM2 = 13
SCHE1 = 19
SCHE2 = 6
#I2C
SDAP = 2
SCLP = 3
HGB = 4
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
#Movement
FORWARD, BACKWARD, STOP = range(0,2)
#Steps
SCHTZKPPSCHLTR, RTNKNPFDRCKN, QUTTNGNTNHMN, OFF = range(3,6)
#otherstuff
counterfile = "/home/pi/counter.txt"
CRCL = "\n"


#Vars
cntr = 0


#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Scheren pins
GPIO.setup([SCHM1, SCHM2], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([SCHE1, SCHE2], GPIO.IN)
#Perry
GPIO.setup([RTKNPF, HNDNDSCHLTR, RTSCHLTR, NEBEL], GPIO.IN)
#Hand
GPIO.setup([EN, INA, INB], GPIO.OUT, initial=GPIO.LOW)
#Shutdown
GPIO.setup(SHTDWN, GPIO.IN)

#Event detect
GPIO.add_event_detect(SHTDWN, GPIO.FALLING)


#Startup IO
if not(os.path.isfile(counterfile)):
    fl = open(counterfile, "w")
    fl.write("0" + CRCL)
    fl.close()

cntrfl = open(counterfile, "r")
cntr = int(cntrfl.readline)
cntrfl.close()



def shutdown(channel):
    time.sleep(0.2)
    if GPIO.input(channel) == 0:
        os.system("shutdown -h -t 1")
        quit()

def back_to_idle_in(channel):
    time.sleep(0.2)
    if GPIO.input(channel) == 0:
        asyncio.current_task().cancel()

def schere(action):
    if action == FORWARD:
        GPIO.output(SCHM1, GPIO.HIGH)
        GPIO.output(SCHM2, GPIO.LOW)
    elif action == BACKWARD:
        GPIO.output(SCHM1, GPIO.LOW)
        GPIO.output(SCHM2, GPIO.HIGH)
    else:
        GPIO.output(SCHM1, GPIO.LOW)
        GPIO.output(SCHM2, GPIO.HIGH)

def hand(action):
    if action == FORWARD:
        GPIO.output(EN, GPIO.HIGH)
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
    elif action == BACKWARD:
        GPIO.output(EN, GPIO.HIGH)
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
    else:
        GPIO.output(EN, GPIO.LOW)
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.LOW)

def save_cntr(cntr):
    cntrfl = open(counterfile, 'w')
    cntrfl.write(str(cntr) + CRCL)
    cntrfl.close()

def led_step(step):
    if step == SCHTZKPPSCHLTR:
        GPIO.output(STEP1, GPIO.LOW)
        GPIO.output(STEP2, GPIO.HIGH)
        GPIO.output(STEP3, GPIO.HIGH)
    elif step == RTNKNPFDRCKN:
        GPIO.output(STEP1, GPIO.HIGH)
        GPIO.output(STEP2, GPIO.LOW)
        GPIO.output(STEP3, GPIO.HIGH)
    elif step == QUTTNGNTNHMN:
        GPIO.output(STEP1, GPIO.HIGH)
        GPIO.output(STEP2, GPIO.HIGH)
        GPIO.output(STEP3, GPIO.LOW)
    else:
        GPIO.output(STEP1, GPIO.HIGH)
        GPIO.output(STEP2, GPIO.HIGH)
        GPIO.output(STEP3, GPIO.HIGH)

async def print_qui():
    #Print und so
    #warten und so
    #await asyncio.sleep(1) 
    schere(FORWARD)
    GPIO.wait_for_edge(SCHE1, GPIO.RISING)
    schere(BACKWARD)
    GPIO.wait_for_edge(SCHE2, GPIO.RISING)
    schere(STOP)

async def idle():
    #LED Streifen und Ring fehlt
    while True:
        GPIO.output(WLTSCHRFT, GPIO.LOW)
        await asyncio.sleep(5)
        GPIO.output(WLTSCHRFT, GPIO.HIGH)
        await asyncio.sleep(0.2)

async def rtknpf():
    GPIO.wait_for_edge(RTKNPF, GPIO.RISING)

#Mainloop
async def main(cntr):
    
    while True: 
        #LED Streifen und Ring fehlt
        led_step(STEP1)
        
        idletask = asyncio.create_task(idle())

        GPIO.wait_for_edge(SCHTZKPPSCHLTR, GPIO.RISING)
        #Roter Schalter umgelegt
        idletask.cancel()
        GPIO.output(WLTSCHRFT, GPIO.LOW)
        
        #Schritt 2
        #LED Streifen und Ring fehlt
        led_step(STEP2)
        GPIO.add_event_detect(SCHTZKPPSCHLTR, GPIO.FALLING)
        GPIO.add_event_callback(SCHTZKPPSCHLTR, back_to_idle_in)
        rtknpftask = asyncio.create_task(rtknpf())
        try:
            await rtknpftask
        except asyncio.CancelledError:
            continue
        led_step(OFF)
        cntr += 1
        GPIO.remove_event_detect(SCHTZKPPSCHLTR)

        #Schritt 3
        hand(FORWARD)
        #LED Streifen und Ring fehlt
        GPIO.wait_for_edge(SCHTZKPPSCHLTR, GPIO.FALLING)
        hand(BACKWARD)
        #LED Streifen und Ring fehlt
        led_step(STEP3)
        printtask = asyncio.create_task(print_qui())
        GPIO.wait_for_edge(HNDNDSCHLTR, GPIO.RISING)
        hand(STOP)
        save_cntr(cntr)

        await printtask



#Startup
schere(BACKWARD)
GPIO.wait_for_edge(SCHE1, GPIO.RISING)

hand(BACKWARD)
GPIO.wait_for_edge(HNDNDSCHLTR, GPIO.RISING)



#Add event callbacks
GPIO.add_event_callback(SHTDWN, shutdown)

#Mainloop
asyncio.run(main(cntr))







