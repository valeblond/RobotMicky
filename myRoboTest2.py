#!/usr/bin/env python3
# so that script can be run from Brickman
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from threading import Thread
from time import sleep
from ev3dev2.sound import Sound

# import keyboard

lm = LargeMotor('outA')
lm2 = LargeMotor('outD')
cs = ColorSensor("in1")
cs2 = ColorSensor("in2")
# global cs_black
# global cs2_black
# global i
s = Sound()
s2 = Sound()
cs_black = {'0': False}
cs2_black = {'0': False}
# cs2_black = False
i = {'0': 0}

# to measure reflected light intensity. In this mode the sensor will return a value between 0 and 100
cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'


def notBlack(cs, cs2):
    while (True):
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



t = Thread(target=notBlack, args=(cs, cs2))
t.start()
# keyboard.is_pressed('ENTER') !=
while (True):
    sleep(1)
    while (cs_black['0'] or cs2_black['0']):
        lm.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")
        lm2.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")
        # lm.run_to_rel_pos(position_sp=50, speed_sp=SpeedPercent(40), stop_action="hold")
        # lm2.run_to_rel_pos(position_sp=50, speed_sp=SpeedPercent(40), stop_action="hold")

    if (i['0'] == 1):
        while (cs_black['0'] == False and cs2_black['0'] == False):
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=3, speed_sp=SpeedPercent(100), stop_action="hold")
            # sleep(5)
            # s.beep()
            # # lm.run_forever(stop_action="hold")
            # # lm2.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")

            # # lm.run_to_rel_pos(position_sp=2, stop_action="hold")
            # # lm2.run_to_rel_pos(position_sp=3, speed_sp=SpeedPercent(100), stop_action="hold")
            pass
    elif (i['0'] == 2):
        while (cs_black['0'] == False and cs2_black['0'] == False):
            lm.run_to_rel_pos(position_sp=3, speed_sp=SpeedPercent(100), stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
            # sleep(5)
            # s2.speak('Hello, I am Robot')
            # # lm.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")
            # # lm2.run_forever(stop_action="hold")

            # # lm.run_to_rel_pos(position_sp=3, speed_sp=SpeedPercent(100), stop_action="hold")
            # # lm2.run_to_rel_pos(position_sp=2, stop_action="hold")
            pass