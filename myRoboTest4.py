from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from threading import Thread
from time import sleep
from ev3dev2.sound import Sound

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

def stan(cs,cs2):
    while (True):
        if (cs.value() < 33 and cs2.value() < 33):
            k['0'] = 1
        elif (cs.value() < 33 and cs2.value() >= 33):
            k['0'] = 2
        elif (cs.value() >= 33 and cs2.value() < 33):
            k['0'] = 3
        elif (cs.value() >= 33 and cs2.value() >= 33):
            k['0'] = 4


t = Thread(target=stan, args=(cs, cs2))
t.start()

sleep(1)
while (True):
    while (k['0'] == 1):        
        sleep(0.2)
        lm.run_forever(speed_sp=200, stop_action="brake")
        lm2.run_forever(speed_sp=200, stop_action="brake")

    if (k['0'] == 2):
        while (k['0'] != 1):
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=3, speed_sp=600, stop_action="hold")
    elif (k['0'] == 3):
        while (k['0'] != 1):
            lm.run_to_rel_pos(position_sp=3, speed_sp=600, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
            


        

