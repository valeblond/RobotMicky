#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep

cs = ColorSensor("in1")
cs2 = ColorSensor("in2")

cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'

while True:
    print("cs.value =  " + str(cs.value()) + ", cs2.value =  " + str(cs2.value()) + "\n")
    sleep(1)