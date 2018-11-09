#!/usr/bin/env python3
# so that script can be run from Brickman
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import MediumMotor
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor
from threading import Thread
from time import sleep
from ev3dev2.sound import Sound

lm = LargeMotor('outA')
lm2 = LargeMotor('outD')
mm = MediumMotor('outC')
cs = ColorSensor("in1")
cs2 = ColorSensor("in2")
ts = TouchSensor("in4")

cs_black = {'0': False}
cs2_black = {'0': False}
i = {'0': 0}    # for black line
k = {'0': 0}    # for blue line
lugIn = False

# to measure reflected light intensity. In this mode the sensor will return a value between 0 and 100
cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'

def takeLuggage():
    pass

def notBlack(cs, cs2):
    while (True):
        if (cs.value() < SOMEVAL and cs.value() > SOMEVAL):      # SOMEVAL for blue color
            k['0'] = 1
            continue
        if (cs2.value() < SOMEVAL and cs2.value() > SOMEVAL):    # SOMEVAL for blue color
            k['0'] = 1
            continue

        if (k['0'] == 1 and cs.value() < SOMEVAL and cs.value() > SOMEVAL):   # SOMEVAL for blue color
            k['0'] = 2
            continue
        if (k['0'] == 1 and cs2.value() < SOMEVAL and cs2.value() > SOMEVAL): # SOMEVAL for blue color
            k['0'] = 2
            continue

        if (cs.value() < 20):
            cs_black['0'] = True
            if (cs_black['0'] and cs2_black['0'] == False):
                i['0'] = 1
        else:
            cs_black['0'] = False

        if (cs2.value() < 20):
            cs2_black['0'] = True
            if (cs2_black['0'] and cs_black['0'] == False):
                i['0'] = 2
        else:
            cs2_black['0'] = False

def alongBlue():
    pass

def alongBlack():
    #while(True):
        while (cs_black['0'] or cs2_black['0']):
            lm.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")
            lm2.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")

        if (k['0'] == 1 or k['0'] == 2):
            alongBlue()

        if (i['0'] == 1):
            while (cs_black['0'] == False and cs2_black['0'] == False):
                lm.run_to_rel_pos(position_sp=0, stop_action="hold")
                lm2.run_to_rel_pos(position_sp=3, speed_sp=SpeedPercent(100), stop_action="hold")

            pass
        elif (i['0'] == 2):
            while (cs_black['0'] == False and cs2_black['0'] == False):
                lm.run_to_rel_pos(position_sp=3, speed_sp=SpeedPercent(100), stop_action="hold")
                lm2.run_to_rel_pos(position_sp=0, stop_action="hold")

            pass

t = Thread(target=notBlack, args=(cs, cs2))
t.start()

while (True):
    sleep(1)
    alongBlack()