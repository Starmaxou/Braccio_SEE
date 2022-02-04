from pickle import FALSE, TRUE

from main import Base, Shoulder, Elbow, WristVer, WristRot, Gripper

class OscCallbacks:
    def egg_control(self, str, args, *stArgs):
        _Activation = args
        print("EggControl :", _Activation)
        # TODO Insérer ici la fonction à appeler pour exécuter la commande
    
    def move_base(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveBase -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        # TODO Insérer ici la fonction à appeler pour exécuter la commande
    
    def move_shoulder(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveShoulder -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        # TODO Insérer ici la fonction à appeler pour exécuter la commande
    
    def move_elbow(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveElbow -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        # TODO Insérer ici la fonction à appeler pour exécuter la commande
        
    def move_wrist_ver(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveWristVer -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        # TODO Insérer ici la fonction à appeler pour exécuter la commande

    def move_wrist_rot(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveWristRot -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        # TODO Insérer ici la fonction à appeler pour exécuter la commande

    def move_gripper(self, str, args, *stArgs):
        _targetAngle = args
        _timeToReach = stArgs[0]
        _accelTime = stArgs[1]
        print("MoveGripper -> targetAngle :", _targetAngle, " timeToReach :", _timeToReach, "accelTime", _accelTime)
        # TODO Insérer ici la fonction à appeler pour exécuter la commande