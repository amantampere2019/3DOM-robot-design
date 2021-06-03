#!/usr/bin/env python
# Inspiration from
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# 
#
# This code is for running a robot of 3 DOM.
# 
# Hardware: Connect NXT motors and sensors to the BrickPi3. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  By running this program, robot identifies and locates the pieces as well as stack them in predefined color order.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers


def closeGripper():
        try:                                        #sometime that doesn't work, and block everything so I put a block "try"
            touch = BP.get_sensor(BP.PORT_1)        #We read the value of touch sensor for initialise the while boucle
            print (touch) 
        except brickpi3.SensorError as error:
            print(error)
        i = BP.get_motor_encoder(BP.PORT_A)         #i prend la valeur de la position du moteur3, 
        while touch != 1:                       #We close the end effector until touch sensor say ok
            i = i - 10
            BP.set_motor_position(BP.PORT_A, i)
            time.sleep(0.2)
            try:
                touch = BP.get_sensor(BP.PORT_1)        #We read the value of touch sensor for do the while boucle
                print (touch)
            except brickpi3.SensorError as error:
                print(error)
              
                
BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
positionlego1 = -400
positionlego2 = -800
positionlego3 = -1200

try:
    while True:
        try: #initialisation
            BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) # reset encoder B
            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) # reset encoder C
            BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)  #Sensor type sensor light
            BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)         #Sensor type sensor touch
            BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH)
            #BP.set_motor_position(BP.PORT_C, 90)                        We up the motor 2 
            #BP.set_motor_position(BP.PORT_A, 60)                        We open the end effector

            BP.set_motor_power(BP.PORT_C, BP.MOTOR_FLOAT)
            BP.set_motor_limits(BP.PORT_C, 90, 150)
            BP.set_motor_power(BP.PORT_B, BP.MOTOR_FLOAT)
            #BP.set_motor_limits(BP.PORT_B, 70, 220)
            BP.set_motor_power(BP.PORT_A, BP.MOTOR_FLOAT)
            BP.set_motor_limits(BP.PORT_A, 90, 140)
            
        except IOError as error:
            print("error reset")
            
        try:
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 90)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_A, 60)
            time.sleep(2)
            try:
                value = BP.get_sensor(BP.PORT_3)
                print(value)
            except brickpi3.SensorError as error:
                print(error)
                value = 0

            while value!=1:
            
                try:
                    value = BP.get_sensor(BP.PORT_3)
                    print(value)
                except brickpi3.SensorError as error:
                    print(error)
                    value = 0
                speed=50
                BP.set_motor_power(BP.PORT_B, speed)
                time.sleep(0.02)
            

        except IOError as error:
            print("error reset")


        
        try:

            BP.set_motor_power(BP.PORT_B, BP.MOTOR_FLOAT)
            #BP.set_motor_limits(BP.PORT_B, 70, 100)
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            time.sleep(2)
            print("moving")
            BP.set_motor_position(BP.PORT_B, positionlego1)   #We reach the first position 
            print("done")
            time.sleep(1)                                   #Wait to be sure we are in position
            BP.set_motor_position(BP.PORT_C, 0)             #We put down the en effector
            time.sleep(1)                                   #Wait to be sure we are in position
            closeGripper()                                  #We close the end effector until touch sensor say ok

            
        except IOError as error:
            print("error reset")
            
        try:                                    #sometime that doesn't work, and block everything so I put a block "try"
            value = BP.get_sensor(BP.PORT_2) #We read the value of light sensor to know if the lego is orange or blue
            print (value) 
        except brickpi3.SensorError as error:
            print(error)

        if  value > 2200:   #We have to determinate the valeur to know if it's blue or orange, here it's blue so we are in situation 1 (Blue - Orange - Orange)  

            #It's blue so we don't care
            BP.set_motor_position(BP.PORT_A, 60)
            time.sleep(2)#We open the end effector 
            BP.set_motor_position(BP.PORT_C, 90)
            time.sleep(2)#We up the motor 2

            
            #We go to the position 3 
            BP.set_motor_position(BP.PORT_B, positionlego3)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 0)             #We put down the en effector
            time.sleep(2)                                 #Wait to be sure we are in position


            closeGripper()                              #calling closeGripper function
            
            BP.set_motor_position(BP.PORT_C, 100) #We put at position 0 the orange lego
            time.sleep(2)
            BP.set_motor_position(BP.PORT_B, 0)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 0)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_A, 60)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 90) 
            time.sleep(2)

            
            BP.set_motor_position(BP.PORT_B, positionlego1) #We comeback to the first position
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 0)
            time.sleep(2)
            closeGripper()                                 #We close the end effector until touch sensor say ok
            BP.set_motor_position(BP.PORT_C, 100)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_B, 0)    #We go to the position 0
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 50) #default 20
            time.sleep(2)
            BP.set_motor_position(BP.PORT_A, 60)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 120) 
            time.sleep(2)




            
            BP.set_motor_position(BP.PORT_B, positionlego2)      #We go to the second position
            time.sleep(1)
            BP.set_motor_position(BP.PORT_C, 0)             #We put down the en effector
            time.sleep(1)                                   #Wait to be sure we are in position
            closeGripper()
            BP.set_motor_position(BP.PORT_C, 110)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_B, 0)           #We go to the position 0 
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 70)            #default 40
            time.sleep(2)
            BP.set_motor_position(BP.PORT_A, 60)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 120)            #default 90
            time.sleep(2)

        else:
            #it's orange, we put on 0 position
            BP.set_motor_position(BP.PORT_C, 100)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_B, 0)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 0)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_A, 50)          #We open the end effector
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 90)                        #We up the motor 2
            time.sleep(2)

            
            #We go to the position 2
            BP.set_motor_position(BP.PORT_B, positionlego2)
            time.sleep(2)
            BP.set_motor_position(BP.PORT_C, 0)             #We put down the en effector
            time.sleep(2)    

            #We close the end effector
            closeGripper()

            #We take the value of light sensor 
            try:                                    #sometime that doesn't work, and block everything so I put a block "try"
                value = BP.get_sensor(BP.PORT_2) #We read the value of light sensor to know if the lego is orange or blue
                print (value) 
            except brickpi3.SensorError as error:
                print(error)



            if value > 2200:        #if it's blue we take and this is the last condition (we are in situation 2 orange blue orange) 
                
                BP.set_motor_position(BP.PORT_C, 100) #We put at position target (0) the blue lego
                time.sleep(2)
                BP.set_motor_position(BP.PORT_B, 0)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 50)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_A, 50)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 120) 
                time.sleep(2)


                #We put the last lego on target position
                #First we reach the last position (position 3) 
                BP.set_motor_position(BP.PORT_B, positionlego3)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 0)
                time.sleep(2)

                #We close the end effector
                closeGripper()

                BP.set_motor_position(BP.PORT_C, 110)       #default 90
                time.sleep(2)

                
                #Second we reach the target position 
                BP.set_motor_position(BP.PORT_B, 0)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 80)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_A, 50)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 120) 
                time.sleep(2)

                
            else:                                         #we are in situation 3 (orange orange blue) 
                print("take the blue lego in position 3") 
                #It's orange so we don't care
                #We open the end effector 
                BP.set_motor_position(BP.PORT_A, 50)
                time.sleep(2)                                               #We open the end effector 
                BP.set_motor_position(BP.PORT_C, 100)                        #We up the motor 2
                time.sleep(2)

                #We reach position 3 to take the blue lego
                BP.set_motor_position(BP.PORT_B, positionlego3)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 0)
                time.sleep(2)

                #We close the end effector
                closeGripper()

                BP.set_motor_position(BP.PORT_C, 90)
                time.sleep(2)       
                BP.set_motor_position(BP.PORT_B, 0)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 50)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_A, 50)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 120) 
                time.sleep(2)

                #We go to the second position to take the last lego
                BP.set_motor_position(BP.PORT_B, positionlego2)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 0)
                time.sleep(2)

                #We close the end effector
                closeGripper()

                BP.set_motor_position(BP.PORT_C, 110)
                time.sleep(2)       
                BP.set_motor_position(BP.PORT_B, 0)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 70)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_A, 50)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 130) 
                time.sleep(2)

                #We go to the target position (0) 
                BP.set_motor_position(BP.PORT_B, -1500)
                """time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 70)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_A, 50)
                time.sleep(2)
                BP.set_motor_position(BP.PORT_C, 110) 
                time.sleep(2)"""

        
        BP.set_motor_position(BP.PORT_B, -1400)
        time.sleep(10)
        BP.set_motor_position(BP.PORT_A, 0)
        time.sleep(1)
        BP.set_motor_position(BP.PORT_C, 0)
        time.sleep(5)
        BP.reset_all()     
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()
    
