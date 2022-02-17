import subprocess
from os import O_SYNC
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

from motor.Motor import Motor
from motor.MotorPID import MotorPID
from motor.myConstants import *

Base = MotorPID("MX106T", 0, MOTOR_PORT, BAUDRATE)
Shoulder = MotorPID("MX106T", 1, MOTOR_PORT, BAUDRATE)
Elbow = MotorPID("MX64T", 2, MOTOR_PORT, BAUDRATE)
WristVer = MotorPID("MX28T", 3, MOTOR_PORT, BAUDRATE)
WristRot = Motor("AX18A", 4, MOTOR_PORT, BAUDRATE)
Gripper = Motor("AX18A", 5, MOTOR_PORT, BAUDRATE)

class OscCallbacks :
    def egg_control(self, str, args, *stArgs):
        _Activation = args
        print("EggControl :", _Activation)
        

    def move_base(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        print("MoveBase -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach)
        Base.move(_targetAngle, _timeToReach, True)

    def move_shoulder(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveShoulder -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach)
        Shoulder.move(_targetAngle, _timeToReach, True)

    def move_elbow(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveElbow -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach)
        Elbow.move(_targetAngle, _timeToReach, True)
        
    def move_wrist_ver(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveWristVer -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach)
        WristVer.move(_targetAngle, _timeToReach, True)

    def move_wrist_rot(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveWristRot -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach)
        WristRot.move(_targetAngle, _timeToReach, True)

    def move_gripper(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveGripper -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach)
        Gripper.move(_targetAngle, _timeToReach, True)


Call = OscCallbacks

parser = argparse.ArgumentParser()
parser.add_argument("--ip",default="192.168.145.172", help="the ip to listen on")
parser.add_argument("--port", type=int, default=5005,help="the ip to listen on")
args = parser.parse_args()

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/EggControl",Call.egg_control,"activation")
dispatcher.map("/Move/Base",Call.move_base,"targetAngle", "timeToReach")
dispatcher.map("/Move/Shoulder",Call.move_shoulder,"targetAngle", "timeToReach")
dispatcher.map("/Move/Elbow",Call.move_elbow,"targetAngle", "timeToReach")
dispatcher.map("/Move/WristVer",Call.move_wrist_ver,"targetAngle", "timeToReach")
dispatcher.map("/Move/WristRot",Call.move_wrist_rot,"targetAngle", "timeToReach")
dispatcher.map("/Move/Gripper",Call.move_gripper,"targetAngle", "timeToReach")

server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
#client = udp_client.SimpleUDPClient(args.ip, args.port)

print("Serving on {}".format(server.server_address))

server.serve_forever()
subprocess.call("./OSC/osc_serv.py", shell = True)

