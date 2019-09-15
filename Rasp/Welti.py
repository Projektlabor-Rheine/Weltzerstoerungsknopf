#!/usr/bin/python


#DDDASSSS Selbstzerstörungsskript

import RPi.GPIO as GPIO
import time
import os.path
import os
import asyncio
from functools import partial
from escpos.printer import Usb
import random


#CONST
#Shutdown
#IO14 is already handled
SHTDWN = 15
#schere
SCHM1 = 26
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
FORWARD, BACKWARD, STOP = range(0,3)
#Steps
SCHTZKPPSCHLTR, RTNKNPFDRCKN, QUTTNGNTNHMN, OFF = range(4,8)
#otherstuff
counterfile = "/home/pi/Welti/counter.txt"
CRCL = "\n"


#Vars
cntr = 0


#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Scheren pins
GPIO.setup([SCHM1, SCHM2, NEBEL], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([SCHE1, SCHE2], GPIO.IN)
#Perry
GPIO.setup([RTKNPF, HNDNDSCHLTR, RTSCHLTR], GPIO.IN)
#Hand
GPIO.setup([EN, INA, INB], GPIO.OUT, initial=GPIO.LOW)
#LED schrift
GPIO.setup([WLTSCHRFT, STEP1, STEP2, STEP3], GPIO.OUT, initial=GPIO.HIGH)
#Shutdown
GPIO.setup(SHTDWN, GPIO.IN)

#Event detect
GPIO.add_event_detect(SHTDWN, GPIO.FALLING)

#Printer setupo
p = Usb(0x0416, 0x5011)

#Startup IO
if not(os.path.isfile(counterfile)):
    fl = open(counterfile, "w")
    fl.write("0" + CRCL)
    fl.close()

cntrfl = open(counterfile, "r")
cntr = int(cntrfl.readline())
cntrfl.close()



def shutdown(channel):
    time.sleep(0.2)
    if GPIO.input(channel) == 0:
        os.system("shutdown -t 1")
        quit()

def back_to_idle_in(channel, task):
    time.sleep(1)
    if GPIO.input(channel) == 1:
        print("back to idle trigerred")
        print(task)
        task.cancel()
        GPIO.remove_event_detect(RTKNPF)

def schere(action):
    print("schere")
    if action == FORWARD:
        print("juergen")
        GPIO.output(SCHM1, GPIO.HIGH)
        GPIO.output(SCHM2, GPIO.LOW)
    elif action == BACKWARD:
        print("joachim")
        GPIO.output(SCHM1, GPIO.LOW)
        GPIO.output(SCHM2, GPIO.HIGH)
    else:
        print("waldemar")
        GPIO.output(SCHM1, GPIO.LOW)
        GPIO.output(SCHM2, GPIO.LOW)

def hand(action):
    if action == FORWARD:
        GPIO.output(EN, GPIO.HIGH)
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
    elif action == BACKWARD:
        GPIO.output(EN, GPIO.HIGH)
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
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

async def print_qui(cntr):
    #Print und so
    print("Druckauftrag: " + str(cntr))
    p.text(" Sie sind der " + str(cntr) + ". der seit Anfang der MAKER FAIRE HANNOVER 2019 \n die Welt zerstoeren wollte!")
    p.text("\n")
    ran = random.randint(1, 101)
    if cntr == 666:
        p.image("/home/pi/Welti/Bernsen.png")
        p.text("Muhahahahaha")
    else:
        p.image("/home/pi/Welti/Pilzi.png")
    if ran == 42:
        p.image("/home/pi/Welti/Afting.jpeg")
        p.text("Herzlichen Glueckwunsch, sie haben einen Glücks-Afting bekommen. Kommen sie zum Projektlabor-stand und lösen sie diese Quittung gegen ein kleines Geschenk ein")
    p.text("\n")
    p.cut()
    #warten und so
    #await asyncio.sleep(1) 
    print("print und so")
    schere(FORWARD)
    GPIO.wait_for_edge(SCHE2, GPIO.RISING)
    schere(BACKWARD)
    GPIO.wait_for_edge(SCHE1, GPIO.RISING)
    schere(STOP)

async def idle():
    #LED Streifen und Ring fehlt
    while True:
        GPIO.output(WLTSCHRFT, GPIO.LOW)
        await asyncio.sleep(5)
        GPIO.output(WLTSCHRFT, GPIO.HIGH)
        await asyncio.sleep(0.2)

async def rtknpf():
    print("rtknpf task is running")
    GPIO.add_event_detect(RTKNPF, GPIO.FALLING)
    while True:
        if GPIO.event_detected(RTKNPF):
            pass
        await asyncio.sleep(0.5)
        if GPIO.input(RTKNPF) == 0:
            GPIO.remove_event_detect(RTKNPF)
            return

async def nebelshuht(cntr):
    GPIO.output(NEBEL, GPIO.HIGH)
    if cntr == 666:
        await asyncio.sleep(5)
    else:
        await asyncio.sleep(0.25)
    GPIO.output(NEBEL, GPIO.LOW)
    await asyncio.sleep(0.05)

#Mainloop
async def main(cntr):
    
    while True: 
        print("inside main loop")
        #LED Streifen und Ring fehlt
        led_step(STEP1)
        
        idletask = asyncio.create_task(idle())
        print("idletask started")
        GPIO.remove_event_detect(RTSCHLTR)
        GPIO.wait_for_edge(RTSCHLTR, GPIO.FALLING)
        GPIO.remove_event_detect(RTSCHLTR)
        #Roter Schalter umgelegt
        idletask.cancel()
        GPIO.output(WLTSCHRFT, GPIO.LOW)
        
        #Schritt 2
        #LED Streifen und Ring fehlt
        led_step(STEP2)
        #iwie task übergebn
        rtknpftask = asyncio.create_task(rtknpf())
        GPIO.add_event_detect(RTSCHLTR, GPIO.RISING, callback=partial(back_to_idle_in, task=rtknpftask))
        print("task created")
        try:
            print("awaiting...")
            await rtknpftask
            print("awaited")
        except asyncio.CancelledError:
            print("continued")
            continue
        led_step(OFF)
        cntr += 1
        GPIO.remove_event_detect(RTSCHLTR)
        #Schritt 3
        hand(FORWARD)
        nebeltask = asyncio.create_task(nebelshuht(cntr))
        print("hand forward")
        #LED Streifen und Ring fehlt
        while True:
            GPIO.wait_for_edge(RTSCHLTR, GPIO.RISING)
            await asyncio.sleep(0.5)
            if GPIO.input(RTSCHLTR) == 1:
                break
        GPIO.remove_event_detect(RTSCHLTR)
        hand(BACKWARD)
        #LED Streifen und Ring fehlt
        led_step(STEP3)
        printtask = asyncio.create_task(print_qui(cntr))
        while True:
            GPIO.wait_for_edge(HNDNDSCHLTR, GPIO.FALLING)
            await asyncio.sleep(0.5)
            if GPIO.input(HNDNDSCHLTR) == 0:
                break
        hand(STOP)
        await asyncio.sleep(1)
        print("handstopped")
        save_cntr(cntr)

        await printtask



#Startup
print("startup")
if GPIO.input(SCHE1) == 0:
    schere(BACKWARD)
    GPIO.wait_for_edge(SCHE1, GPIO.RISING)
    schere(STOP)

print("schere ok")

if GPIO.input(HNDNDSCHLTR) == 1:
    hand(BACKWARD)
    GPIO.wait_for_edge(HNDNDSCHLTR, GPIO.FALLING)
    hand(STOP)

print("hand ok")

#Add event callbacks
GPIO.add_event_callback(SHTDWN, shutdown)

print("before main loop")

#Mainloop
asyncio.run(main(cntr))







