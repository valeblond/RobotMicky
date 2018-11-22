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
q = {'0': 0}
z = {'0': 0}

# to measure reflected light intensity. In this mode the sensor will return a value between 0 and 100
cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'


def stan(cs, cs2):
    while True:
        # dla zwyklej jazdy
        if (cs.value() <= 33 and cs.value() > 20): #jechac prosto
            z['0'] = 1
            print("1" + "\n" + "\n")
        elif (cs.value() <= 20): #troche skrecic w lewo(za duzo czarnego)
            print("2" + "\n" + "\n")
            z['0'] = 2
        elif (cs.value() > 33): #troche skrecic w prawo(za malo czarnego)
            print("3" + "\n" + "\n")
            z['0'] = 3

        # dla powrotow i skrzyzowan
        if (cs.value() < 20 and cs2.value() < 20):  # jechac prosto (na skrzyzowaniu)
            print("4" + "\n" + "\n")
            q['0'] = 1
#        elif (cs.value() < 15 and cs2.value() >= 37):  # skret w lewo
 #           q['0'] = 2
  #      elif (z['0'] == 1 and cs2.value() < 15):  # skret w prawo
   #         q['0'] = 3
    #    elif (cs.value() > 33  and cs2.value() < 25):  # skret w prawo
     #       q['0'] = 4
        elif True:
            q['0'] = 0
            print("5" + "\n" + "\n")

t = Thread(target=stan, args=(cs, cs2))
t.start()

sleep(1)
while True:
    while ((z['0'] == 1 or q['0'] == 1) and q['0'] != 2 and q['0'] != 3 ):
    	lm.run_forever(speed_sp=200, stop_action="hold")
    	lm2.run_forever(speed_sp=200, stop_action="hold")
    print("6" + "\n")

    if (z['0'] == 2 and q['0'] == 0):
        while (z['0'] != 1 or q['0'] != 1):
            lm.run_forever(speed_sp=0, stop_action="hold")
            lm2.run_forever(speed_sp=100, stop_action="hold")
        lm.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")       
        print("7" + "\n" + "\n")
        continue
    elif (z['0'] == 3 and q['0'] == 0):
        while (z['0'] != 1):
            lm2.run_forever(speed_sp=0, stop_action="hold")
            lm.run_forever(speed_sp=100, stop_action="hold")
        lm.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")       
        print("8" + "\n" + "\n")
        continue
#    elif (q['0'] == 3):
  #      while (cs2.value() < 20):
   #         lm2.run_forever(speed_sp=0, stop_action="hold")
    #        lm.run_forever(speed_sp=100, stop_action="hold")
     #   continue
 #   elif (q['0'] == 2):
  #      while (cs.value() < 20):
   #         lm.run_forever(speed_sp=0, stop_action="hold")
    #        lm2.run_forever(speed_sp=100, stop_action="hold")
     #   continue
