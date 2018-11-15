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
dt = 500 
Kp = 1  # proportional gain
Ki = 0  # integral gain
Kd = 0  # derivative gain

integral = 0
previous_error = 0
#target_value = cs.value()
mid = cs.value()
def notBlack(cs, cs2):
    while (True):
        if (cs.value() < 30):
            cs_black['0'] = True
            if (cs_black['0'] and cs2_black['0'] == False):
                i['0'] = 1
        else:
            cs_black['0'] = False

        if (cs2.value() < 30):
            cs2_black['0'] = True
            if (cs2_black['0'] and cs_black['0'] == False):
                i['0'] = 2
        else:
            cs2_black['0'] = False

error = mid - cs.value()
integral = 0.5 * integral + error 
last_error = error
derivative = error - last_error

#error = target_value - cs.value()
#integral += (error * dt)
#derivative = (error - previous_error) / dt
u = (Kp * error) + (Ki * integral) + (Kd * derivative)
correction = int(0.7 * error + 0.25 * integral + 7.0 * derivative)


t = Thread(target=notBlack, args=(cs, cs2))
t.start()

sleep(1)
while (True):
    while (cs_black['0'] or cs2_black['0']):
        if(k['0'] == 1):
            #lm.run_forever(speed_sp=0, stop_action="hold")
            #lm2.run_forever(speed_sp=0, stop_action="hold")
            lm.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=45, speed_sp=900, stop_action="hold")
        elif(k['0'] == 2):
            #lm.run_forever(speed_sp=0, stop_action="hold")
            #lm2.run_forever(speed_sp=0, stop_action="hold")
            lm.run_to_rel_pos(position_sp=45, speed_sp=900, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        
        sleep(0.2)
#        lm.run_to_rel_pos(position_sp=45, speed_sp=900, stop_action="hold")
#        lm2.run_to_rel_pos(position_sp=0, speed_sp=0, stop_action="hold")
        lm.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")
        lm2.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")

    if (i['0'] == 1):
        while (cs_black['0'] == False and cs2_black['0'] == False):
            #lm.run_forever(speed_sp=0, stop_action="hold")
            #lm2.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")
            lm.run_to_rel_pos(position_sp=0, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=15, speed_sp=900, stop_action="hold")
            k['0'] == 1
            
            
        
    elif (i['0'] == 2):
        while (cs_black['0'] == False and cs2_black['0'] == False):
            #lm.run_forever(speed_sp=SpeedPercent(100), stop_action="hold")
            #lm2.run_forever(speed_sp=0, stop_action="hold")
            lm.run_to_rel_pos(position_sp=15, speed_sp=900, stop_action="hold")
            lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
            k['0'] == 2
