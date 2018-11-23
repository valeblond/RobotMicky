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
cs_black = {'0': False}
cs2_black = {'0': False}
i = {'0': 0}
k = {'0': 0}

# to measure reflected light intensity. In this mode the sensor will return a value between 0 and 100
cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'


def notBlack(cs, cs2):
    while (True):
        if (cs.value() < 30):
            cs_black['0'] = True
            if (cs_black['0'] and cs2_black['0'] == False):
                i['0'] = 1
        else:
            cs_black['0'] = False

        if (cs2.value() < 30):
            cs2_black['0'] = True
            if (cs2_black['0'] and cs_black['0'] == False):
                i['0'] = 2
        else:
            cs2_black['0'] = False

        if(cs.value() < 26 or cs2.value() < 26):
            if (cs.value() > 10 and cs.value() < 30 and cs2.value() < 10): # turn right
                k['0'] == 1

            if (cs.value() < 10 and cs2.value() > 10 and cs2.value() < 30): # turn left
                k['0'] == 1

            if (cs.value() < 26 and cs2.value() < 26):
                if(cs.value() > cs2.value()):
                    k['0'] == 3             # turn right
                else:
                    k['0'] == 4             # turn left
        else:
            k['0'] == 0

t = Thread(target=notBlack, args=(cs, cs2))
t.start()

sleep(1)
while (True):
    while ((cs_black['0'] or cs2_black['0']) and k['0'] == 0):
        sleep(0.4)
        lm.run_forever(speed_sp=150, stop_action="hold")
        lm2.run_forever(speed_sp=150, stop_action="hold")

    lm.stop(stop_action="hold")
    lm2.stop(stop_action="hold")

    if (i['0'] == 1 and k['0'] == 0):
        while (cs_black['0'] == False and cs2_black['0'] == False):
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=7, speed_sp=200, stop_action="hold")
        lm.run_to_rel_pos(position_sp=2, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=30, speed_sp=500, stop_action="hold")
    elif (i['0'] == 2 and k['0'] == 0):
        while (cs_black['0'] == False and cs2_black['0'] == False):
            lm.run_to_rel_pos(position_sp=7, speed_sp=200, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
        lm.run_to_rel_pos(position_sp=30, speed_sp=500, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=2, stop_action="hold")

    if(k['0'] == 1 or k['0'] == 3):     # turn right
        while(k['0'] != 0):
            lm.run_to_rel_pos(position_sp=7, speed_sp=200, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
        lm.run_to_rel_pos(position_sp=30, speed_sp=500, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=2, stop_action="hold")
    elif(k['0'] == 2 or k['0'] == 4):   # turn left
        while(k['0'] != 0):
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=7, speed_sp=200, stop_action="hold")
        lm.run_to_rel_pos(position_sp=2, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=30, speed_sp=500, stop_action="hold")

