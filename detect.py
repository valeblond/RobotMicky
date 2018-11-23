#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from threading import Thread
from time import sleep
from ev3dev.ev3 import *

lm = LargeMotor('outA')
lm2 = LargeMotor('outD')
cs = ColorSensor("in1")
cs2 = ColorSensor("in2")
ir = InfraredSensor("in3")

# to measure reflected light intensity. In this mode the sensor will return a value between 0 and 100
cs.mode = 'COL-COLOR'
cs2.mode = 'COL-COLOR'
# Put the infrared sensor into proximity mode.
ir.mode = 'IR-PROX'

q = {'0': 0} # For detecting what color he has found
k = {'0': 0} # For detecting if we are close to some other object
i = {'0': 0} # For detecting if we've already made a round for needed color

def distan(ir, l):
    while (True):
        if(ir.value() > 25):
            k['0'] = 1     # okay
        else:
            k['0'] = 2     # need turn

def notBlack(cs, cs2):
    while (True):
        if ((cs.value() == 5 or cs2.value() == 5) and q['0'] == 0): # Find red color
            q['0'] = 1
        if ((cs.value() == 2 or cs2.value() == 2) and q['0'] == 1): # Find blue color
            q['0'] = 2
        if ((cs.value() == 3 or cs2.value() == 3) and q['0'] == 2): # Find green color
            q['0'] = 3
        if ((cs.value() == 4 or cs2.value() == 4) and q['0'] == 3): # Find yellow color
            q['0'] = 4

t = Thread(target=notBlack, args=(cs, cs2))
d = Thread(target=distan, args=(ir, 0))
t.start()
d.start()

sleep(1)
while (True):
    print()
    while (k['0'] == 1 and q['0'] == 0):       # Looking for red square
        lm.run_forever(speed_sp=400, stop_action="hold")
        lm2.run_forever(speed_sp=400, stop_action="hold")
    if (k['0'] == 1 and q['0'] == 1 and i['0'] == 0):          # When he's found red color
        i['0'] = 1
        Sound.beep()
        print("r")
        lm.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=30, speed_sp=800, stop_action="hold")
        sleep(4)
    while (k['0'] == 1 and q['0'] == 1):       # Looking for blue square
        lm.run_forever(speed_sp=400, stop_action="hold")
        lm2.run_forever(speed_sp=400, stop_action="hold")
    if (k['0'] == 1 and q['0'] == 2 and i['0'] == 1):          # When he's found blue color
        i['0'] = 2
        Sound.beep()
        print("b")
        lm.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=30, speed_sp=800, stop_action="hold")
        sleep(4)
    while (k['0'] == 1 and q['0'] == 2):       # Looking for green square
        lm.run_forever(speed_sp=400, stop_action="hold")
        lm2.run_forever(speed_sp=400, stop_action="hold")
    if (k['0'] == 1 and q['0'] == 3 and i['0'] == 2):          # When he's found green color
        i['0'] = 3
        Sound.beep()
        print("g")
        lm.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=30, speed_sp=800, stop_action="hold")
        sleep(4)
    while (k['0'] == 1 and q['0'] == 3):       # Looking for yellow square
        lm.run_forever(speed_sp=400, stop_action="hold")
        lm2.run_forever(speed_sp=400, stop_action="hold")
    if (k['0'] == 1 and q['0'] == 4 and i['0'] == 3):          # When he's found yellow color
        i['0'] = 4
        Sound.beep()
        print("y")
        lm.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=30, speed_sp=800, stop_action="hold")
        sleep(4)
    if(k['0'] == 2):
        lm.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=30, speed_sp=800, stop_action="hold")
        sleep(2)




