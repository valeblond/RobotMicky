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

def notBlack(cs,cs2):
    while True:
        #depends on a value of i we'll know which of two sensors was the last one(who detected black color)
        if(cs.reflected_light_intensity < 70):
            cs_black == True
            if(cs_black and cs2_black == False):
                i == 1
        else:
            cs_black == False

        if (cs2.reflected_light_intensity < 70):
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

    if(i==1):
        while(i==1):
            lm.run_to_rel_pos(position_sp=4, speed_sp=SpeedPercent(20), stop_action="hold")
            lm2.run_to_rfacel_pos(position_sp=4, speed_sp=SpeedPercent(20), stop_action="hold")
            if(cs_black or cs2_black):
                break
            else:
                lm.run_to_rel_pos(position_sp=0, stop_action="hold")
                lm2.run_to_rel_pos(position_sp=2, speed_sp=SpeedPercent(20), stop_action="hold")
                break
    elif(i==2):
        while(i==2):
            lm.run_to_rel_pos(position_sp=4, speed_sp=SpeedPercent(20), stop_action="hold")
            lm2.run_to_rel_pos(position_sp=4, speed_sp=SpeedPercent(20), stop_action="hold")
            if (cs_black or cs2_black):
                break
            else:
                lm.run_to_rel_pos(position_sp=2, speed_sp=SpeedPercent(20), stop_action="hold")
                lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
                break
