from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from threading import Thread
from time import sleep
import keyboard

lm = LargeMotor('outA')
lm2 = LargeMotor('outB')
cs = ColorSensor("in1")
cs2 = ColorSensor("in2")
cs_black = False
cs2_black = False
i = 0

# to measure reflected light intensity. In this mode the sensor will return a value between 0 and 100
cs.mode = 'COL-REFLECT'
cs2.mode = 'COL-REFLECT'

def notBlack(cs,cs2):
    while True:
        #cs2.reflected_light_intensity < 40
        #depends on a value of i we'll know which of two sensors was the last one(who detected black color)
        if(cs.value < 40):
            cs_black == True
            if(cs_black and cs2_black == False):
                i == 1
        else:
            cs_black == False

        if (cs.value < 40):
            cs2_black == True
            if (cs2_black and cs_black == False):
                i == 2
        else:
            cs2_black == False

t = Thread(target=notBlack, args=(cs,cs2))
t.start()

while(keyboard.is_pressed('ENTER') != True):
    while(cs_black or cs2_black):
        lm.run_to_rel_pos(position_sp=4, speed_sp=SpeedPercent(20), stop_action="hold")
        lm2.run_to_rel_pos(position_sp=4, speed_sp=SpeedPercent(20), stop_action="hold")
        sleep(1)

    lm.run_to_rel_pos(position_sp=4, speed_sp=SpeedPercent(20), stop_action="hold")
    lm2.run_to_rel_pos(position_sp=4, speed_sp=SpeedPercent(20), stop_action="hold")

    if(i==1):
        while(i==1):
            if(cs_black or cs2_black):
                break
            else:
                lm.run_to_rel_pos(position_sp=0, stop_action="hold")
                lm2.run_to_rel_pos(position_sp=2, speed_sp=SpeedPercent(20), stop_action="hold")
                break
    elif(i==2):
        while(i==2):
            if (cs_black or cs2_black):
                break
            else:
                lm.run_to_rel_pos(position_sp=2, speed_sp=SpeedPercent(20), stop_action="hold")
                lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
                break
