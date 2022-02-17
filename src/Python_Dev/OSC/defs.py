from os import O_SYNC
import argparse
import math

class OscCallbacks :
    def egg_control(self, str, args, *stArgs):
        _Activation = args
        print("EggControl :", _Activation)

    def move_base(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveBase -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        Base.move(_targetAngle, _timeToReach, _accelTime, True, False, False)

    def move_shoulder(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveShoulder -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        Shoulder.move(_targetAngle, _timeToReach, _accelTime, True, False, False)

    def move_elbow(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveElbow -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        Elbow.move(_targetAngle, _timeToReach, _accelTime, True, False, False)
        
    def move_wrist_ver(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveWristVer -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        WristVer.move(_targetAngle, _timeToReach, _accelTime, True, False, False)

    def move_wrist_rot(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveWristRot -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        WristRot.move(_targetAngle, _timeToReach, _accelTime, True, False, False)

    def move_gripper(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveGripper -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        Gripper.move(_targetAngle, _timeToReach, _accelTime, True, False, False)
