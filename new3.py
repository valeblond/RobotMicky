from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from threading import Thread
from time import sleep
from ev3dev2.sound import Sound

lm = LargeMotor('outB')
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
Kp = 0.4  # proportional gain
Ki = 0.1  # integral gain
Kd = 0.2  # derivative gain

speed = 360/4
integral = 0
previous_error = 0
target_value = cs.value()
u = 0


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




t = Thread(target=notBlack, args=(cs, cs2))
t.start()


sleep(1)
while (True):
    while (cs_black['0'] or cs2_black['0']):
        sleep(1)
        error = target_value - cs.value()
        integral += (error * dt)
        derivative = (error - previous_error) / dt
        u = (Kp * error) + (Ki * integral) + (Kd * derivative)
        previous_error = error
        
        if speed + abs(u) > 1000:
            if u >= 0:
                u = 1000 - speed
            else:
                u = speed - 1000

        if u >= 0:
            lm.run_forever(speed_sp=speed+u, stop_action="hold")
            lm2.run_forever(speed_sp=speed-u, stop_action="hold")
        else:
            lm.run_forever(speed_sp=speed-u, stop_action="hold")
            lm2.run_forever(speed_sp=speed+u, stop_action="hold")

    lm.stop(stop_action="hold")
    lm2.stop(stop_action="hold")
    
    if (i['0'] == 1):
        while (cs_black['0'] == False and cs2_black['0'] == False):
            error = target_value - cs.value()
            integral += (error * dt)
            derivative = (error - previous_error) / dt
            u = (Kp * error) + (Ki * integral) + (Kd * derivative)
            previous_error = error

            if speed + abs(u) > 1000:
                if u >= 0:
                    u = 1000 - speed
                else:
                    u = speed - 1000

            if u >= 0:
                lm.run_to_rel_pos(position_sp=0, stop_action="hold")
                lm2.run_to_rel_pos(position_sp=7, speed_sp=speed-u, stop_action="hold")
            else:
                lm.run_to_rel_pos(position_sp=0, stop_action="hold")
                lm2.run_to_rel_pos(position_sp=7, speed_sp=speed+u, stop_action="hold")
        lm.run_to_rel_pos(position_sp=0, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=8, speed_sp=600, stop_action="hold")
            
            
        
    elif (i['0'] == 2):
        while (cs_black['0'] == False and cs2_black['0'] == False):
            error = target_value - cs.value()
            integral += (error * dt)
            derivative = (error - previous_error) / dt
            u = (Kp * error) + (Ki * integral) + (Kd * derivative)
            previous_error = error

            if speed + abs(u) > 1000:
                if u >= 0:
                    u = 1000 - speed
                else:
                    u = speed - 1000

            if u >= 0:
                lm.run_to_rel_pos(position_sp=7, speed_sp=speed+u, stop_action="hold")
                lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
            else:
                lm.run_to_rel_pos(position_sp=7, speed_sp=speed-u, stop_action="hold")
                lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
        lm.run_to_rel_pos(position_sp=8, speed_sp=600, stop_action="hold")
        lm2.run_to_rel_pos(position_sp=0, stop_action="hold")
            


        

