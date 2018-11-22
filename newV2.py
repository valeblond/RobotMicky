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
# to measure reflected light intensity. In this mode the sensor will return a value between 0 and 100
cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'

q = {'0': 0}
z = {'0': 0}

Kp = {'0': 1, '1': -1}
Ki = {'0': 0}
Kd = {'0': 0}
target = {'0': 33}
error = {'0': 0}
integ = {'0': 0}
deriv = {'0': 0}
lastError = {'0': 0}
u = {'0': 0}


def stan(cs, cs2):
    while (True):
        # dla zwyklej jazdy
        if (cs.value() <= 33 and cs.value() > 22): #jechac prosto
            z['0'] = 1
        elif (cs.value() < 25): #troche skrecic w lewo(za duzo czarnego)
            z['0'] = 2
        elif (cs.value() > 33): #troche skrecic w prawo(za malo czarnego)
            z['0'] = 3

        # dla powrotow i skrzyzowan
        if (cs.value() < 25 and cs2.value() < 25):  # jechac prosto (na skrzyzowaniu)
            q['0'] = 1
        elif (cs.value() < 15 and cs2.value() >= 37):  # skret w lewo
            q['0'] = 2
        elif (z['0'] == 1 and cs2.value() < 15):  # skret w prawo
            q['0'] = 3
        elif (True):
            q['0'] = 0

t = Thread(target=stan, args=(cs, cs2))
t.start()

sleep(1)
while (True):
    while ((z['0'] == 1 or q['0'] == 1) and q['0'] != 2 and q['0'] != 3 ):
        error['0'] = target['0'] - int(cs.value())
        integ['0'] += error['0']
        deriv['0'] = error['0'] - lastError['0']
        # u zero:     on target,  drive forward
        # u positive: too bright, turn right
        # u negative: too dark,   turn left
        u['0'] = Kp['0']*error['0'] + Ki['0']*integ['0'] + Kd['0']*deriv['0']
        lastError['0'] = error['0']
        
        if(u['0'] >= 0):
            lm.run_forever(speed_sp=200+u['0'], stop_action="hold")
            lm2.run_forever(speed_sp=200-u['0'], stop_action="hold")
        else:
            lm.run_forever(speed_sp=200-u['0'], stop_action="hold")
            lm2.run_forever(speed_sp=200+u['0'], stop_action="hold")

    if (z['0'] == 2 and q['0'] == 0):
        while (z['0'] != 1 or q['0'] != 1):
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=1, speed_sp=400, stop_action="hold")
        continue
    elif (z['0'] == 3 and q['0'] == 0):
        while (z['0'] != 1):
            lm.run_to_rel_pos(position_sp=1, speed_sp=400, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
        continue
    elif (q['0'] == 3):
        while (cs2.value() < 20):
            lm.run_to_rel_pos(position_sp=1, speed_sp=400, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
        continue
    elif (q['0'] == 2):
        while (cs.value() < 20):
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=1, speed_sp=400, stop_action="hold")
        continue
