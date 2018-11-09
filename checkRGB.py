#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
from time import sleep

cs = ColorSensor("in1")
cs2 = ColorSensor("in2")

cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'

while True:
    print(cs.value())
    print(cs2.value())
    sleep(0.5)