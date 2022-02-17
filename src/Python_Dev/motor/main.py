from locale import T_FMT_AMPM
from wsgiref.simple_server import server_version
from myConstants import *
from Motor import *
from MotorPID import *
import random as rand
import time
  
# prints a random value from the list

PORTNAME = "/dev/ttyACM0"
 

#servo_base      = MotorPID("MX106T", 1, PORTNAME, BAUDRATE)
#servo_shoulder  = MotorPID("MX106T", 2, PORTNAME, BAUDRATE)
#servo_elbow     = MotorPID("MX64T", 3, PORTNAME, BAUDRATE)
#servo_wristVer  = MotorPID("MX28T", 4, PORTNAME, BAUDRATE)
#servo_wristRot  = Motor("AX18A", 5, PORTNAME, BAUDRATE)
#servo_gripper   = Motor("AX18A", 6, PORTNAME, BAUDRATE)

servo_base      = MotorPID("MX106T", 0, PORTNAME, BAUDRATE)
servo_shoulder  = MotorPID("MX106T", 1, PORTNAME, BAUDRATE)
servo_elbow     = MotorPID("MX64T", 2, PORTNAME, BAUDRATE)
servo_wristVer  = MotorPID("MX28T", 3, PORTNAME, BAUDRATE)
servo_wristRot  = Motor("AX18A", 4, PORTNAME, BAUDRATE)
servo_gripper   = Motor("AX18A", 5, PORTNAME, BAUDRATE)

tabServo = [servo_base, servo_shoulder, servo_elbow, servo_wristVer, servo_wristRot, servo_gripper]

#servo_base.setP(160)

while (1) :
    #print(servo_base.getPosition())
    #print(servo_base.getLoad())
    #print(servo_base.getMaxSpeed())
    #print(servo_base.getTemperature())
    #print(servo_base.getTorque())
    #print(servo_base.getVoltage())
    servo_elbow.showInfo()

    print("Quel servo controler ?")
    nbServo = int(input())
    if nbServo == 10 :
        servo_base.showInfo()
    else :
        if nbServo < 0 or nbServo > 5 :
            pass
        else:
            print("Quelle position donner ? (en °) ")

            pos = int(input())
            
            print("Quel TTR ?")
            TTR = int(input())
            print("TTR : ", TTR)
            
            print("Quel TTA ?")
            TTA = int(input())
            print("TTA : ", TTA)

            #tabServo[nbServo].setP(0)
            #tabServo[nbServo].setI(0)
            #tabServo[nbServo].setD(0)
            
            if pos < 0 or pos > 360 :
                pass
            else:
                tabServo[nbServo].move(pos, TTR = TTR, TTA=TTA, isDegree=True)
                tabServo[nbServo].getPosition()
        

#servo_base.move(rand.randint(0,360), 10*rand.randint(1,20)/2,isDegree=True)
#servo_shoulder.move(rand.randint(0,360), 10*rand.randint(1,20)/2,isDegree=True)
#servo_elbow.move(rand.randint(0,360), 10*rand.randint(1,20)/2,isDegree=True)
#servo_wristVer.move(rand.randint(0,360), 10*rand.randint(1,20)/2,isDegree=True)
#servo_wristRot.move(rand.randint(0,300), 10*rand.randint(1,20)/2,isDegree=True)
#servo_gripper.move(rand.randint(0,300), 10*rand.randint(1,20)/2,isDegree=True)

#print("Speed : ")
#print(servo_base.getSpeed())

print(servo_base.getPosition())
print(servo_base.getLoad())
print(servo_base.getMaxSpeed())
print(servo_base.getTemperature())
print(servo_base.getTorque())
print(servo_base.getVoltage())