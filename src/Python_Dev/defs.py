from pickle import FALSE, TRUE


class Motor:
    def __init__(self, minAngle, maxAngle):
        currentAngle = self.get_current_angle()
        self._targetAngle = currentAngle
        self._timeToReach = 1
        self._minAngle = minAngle
        self._maxAngle = maxAngle

    def get_current_angle(self):
        _currentAngle = 0 # TODO remplacer le 0 par l'acquisition de l'angle du servo
        return _currentAngle

    def move(self, targetAngle, timeToReach, accelTime):
        self._targetAngle = targetAngle
        self._timeToReach = timeToReach
        self._accelTime = accelTime
        # TODO ajouter appel a la fonction de deplacement du servo ici

    def get_speed(self):
        return self._speed

    def get_load(self):
        return self._load

    def get_voltage(self):
        return self._voltage

    def get_temperature(self):
        return self._temperature

    # Motor parameters for remote OSC control
    _speed = 0
    _load = 0
    _voltage = 0
    _temperature = 0
    

class Braccio:
    
    def egg_control(self, Activation):
        _eggControl = Activation
        print("EGG_CONTROL",Activation)

        # Servo assignment
    Base = Motor(0,0)
    Shoulder = Motor(0,0)
    Elbow = Motor(0,0)
    WristVer = Motor(0,0)
    WristRot = Motor(0,0)
    Gripper = Motor(0,0)

    # Arm control parameters
    _eggControl = FALSE


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