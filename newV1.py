#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from threading import Thread
from time import sleep

lm = LargeMotor('outB')
lm2 = LargeMotor('outD')
cs = ColorSensor("in1")
cs2 = ColorSensor("in2")
cs_black = {'0': False}
cs2_black = {'0': False}
q = {'0': 0}
z = {'0': 0}

# to measure reflected light intensity. In this mode the sensor will return a value between 0 and 100
cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'


def stan(cs, cs2):
    while (True):
        # dla zwyklej jazdy
        if (cs.value() <= 33 and cs.value() > 25): #jechac prosto
            z['0'] = 1
        elif (cs.value() < 25): #troche skrecic w lewo(za duzo czarnego)
            z['0'] = 2
        elif (cs.value() > 33): #troche skrecic w prawo(za malo czarnego)
            z['0'] = 3

        # dla powrotow i skrzyzowan
        if (cs.value() < 25 and cs2.value() < 25):  # jechac prosto (na skrzyzowaniu)
            q['0'] = 1
        elif (cs.value() < 25 and cs2.value() >= 30):  # skret w lewo
            q['0'] = 2
        elif (z['0'] == 1 and cs2.value() < 25):  # skret w prawo
            q['0'] = 3
        elif (True):
            q['0'] = 0

t = Thread(target=stan, args=(cs, cs2))
t.start()

sleep(1)
while (True):
    while ((z['0'] == 1 or q['0'] == 1) and q['0'] != 2 and q['0'] != 3 ):
        lm.run_forever(speed_sp=200, stop_action="hold")
        lm2.run_forever(speed_sp=200, stop_action="hold")

    if (z['0'] == 2 and q['0'] == 0):
        while (z['0'] != 1 or q['0'] != 1):
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=1, speed_sp=600, stop_action="hold")
        continue
    elif (z['0'] == 3 and q['0'] == 0):
        while (z['0'] != 1):
            lm.run_to_rel_pos(position_sp=1, speed_sp=600, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
        continue
    elif (q['0'] == 3):
        while (cs2.value() < 25):
            lm.run_to_rel_pos(position_sp=1, speed_sp=600, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
        continue
    elif (q['0'] == 2):
        while (cs.value() < 25):
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=1, speed_sp=600, stop_action="hold")
        continue
