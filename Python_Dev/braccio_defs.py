from pickle import FALSE, TRUE


class Motor:
    def __init__(self, minAngle, maxAngle):
        currentAngle = self.get_current_angle()
        self.__targetAngle = currentAngle
        self.__timeToReach = 1
        self.__minAngle = minAngle
        self.__maxAngle = maxAngle

    def get_current_angle(self):
        __currentAngle = 0 # TODO remplacer le 0 par l'acquisition de l'angle du servo
        return __currentAngle

    def move(self, targetAngle, timeToReach):
        self.__targetAngle = targetAngle
        self.__timeToReach = timeToReach
        # TODO ajouter appel à la fonction de déplacement du servo ici

    def get_speed(self):
        return self.__speed

    def get_load(self):
        return self.__load

    def get_voltage(self):
        return self.__voltage

    def get_temperature(self):
        return self.__temperature

    # Motor parameters for remote OSC control
    __speed = 0
    __load = 0
    __voltage = 0
    __temperature = 0
    

class Braccio:
    
    def activate_egg_control(self):
        __eggControl = TRUE

    def unactivate_egg_control(self):
        __eggControl = FALSE

    # Servo assignment
    __Base = Motor("Base")
    __Shoulder = Motor("Shoulder")
    __Elbow = Motor("Elbow")
    __WristVer = Motor("Wristver")
    __WristRot = Motor("Wristrot")
    __Gripper = Motor("Gripper")

    # Arm control parameters
    __eggControl = FALSE




