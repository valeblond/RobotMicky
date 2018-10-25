#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

ts = TouchSensor("in3")

while not ts.value():
    pass

Sound.beep() 