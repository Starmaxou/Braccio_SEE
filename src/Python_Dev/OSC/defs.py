from os import O_SYNC
import argparse
import math

from main import Base, Shoulder, Elbow, WristVer, WristRot, Gripper

class OscCallbacks:

    _eggActivated = False

    def egg_control(self, str, args, *stArgs):
        self._eggActivated = args
        print("EggControl :", self._eggActivated)
        # TODO Insérer ici la fonction à appeler pour exécuter la commande
    
    def move_base(self, str, args, *stArgs):
        targetAngle = args
        timeToReach = stArgs[0]
        accelTime = stArgs[1]

        if not(self._eggActivated) :
            Base.move(targetAngle, timeToReach, accelTime, True, False, False)
            print("MoveBase -> targetAngle :", targetAngle, " timeToReach :", timeToReach, "accelTime", accelTime)
    
    def move_shoulder(self, str, args, *stArgs):
        targetAngle = args
        timeToReach = stArgs[0]
        accelTime = stArgs[1]
        if not(self._eggActivated) :
            Shoulder.move(targetAngle, timeToReach, accelTime, True, False, False)
            print("MoveShoulder -> targetAngle :", targetAngle, " timeToReach :", timeToReach, "accelTime", accelTime)


    def move_elbow(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        if not(self._eggActivated) :
            Elbow.move(_targetAngle, _timeToReach, _accelTime, True, False, False)
            print("MoveElbow -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        

    def move_wrist_ver(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        if not(self._eggActivated) :
            WristVer.move(_targetAngle, _timeToReach, _accelTime, True, False, False)
            print("MoveWristVer -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
    

    def move_wrist_rot(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        if not(self._eggActivated) :
            WristRot.move(_targetAngle, _timeToReach, _accelTime, True, False, False)
            print("MoveWristRot -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)


    def move_gripper(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        if not(self._eggActivated) :
            Gripper.move(_targetAngle, _timeToReach, _accelTime, True, False, False)
            print("MoveGripper -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
