import defs
import Motor
import MotorPID
import subprocess
from myConstants import *

Base = MotorPID.MotorPID("MX106T", 1, MOTOR_PORT, BAUDRATE)
Shoulder = MotorPID.MotorPID("MX106T", 2, MOTOR_PORT, BAUDRATE)
Elbow = MotorPID.MotorPID("MX64T", 3, MOTOR_PORT, BAUDRATE)
WristVer = MotorPID.MotorPID("MX28T", 4, MOTOR_PORT, BAUDRATE)
WristRot = Motor.Motor("AX18A", 5, MOTOR_PORT, BAUDRATE)
Gripper = Motor.Motor("AX18A", 6, MOTOR_PORT, BAUDRATE)

subprocess.call("osc_serv.py", shell = True)

