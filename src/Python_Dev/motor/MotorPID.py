from motor.Motor import *

class MotorPID(Motor) :
 
    def __init__(self, motor_reference : string , ID : int, portName : string , CST_BAUDRATE : int) -> None:
        
        if not(motor_reference in MOTORS_INFOS_DICT) :
            print("ERROR    : Motor reference unknown. This class can only handle Dynamixel MX160T, MX64T, MX28T and AX18A")
            print("INFO     : Instanciation aborted")
            return
        elif not(motor_reference in MOTORS_PID_INFOS_DICT) :
            print("WARNING  : You are trying to instanciate a class not corresponding to your motor, use Motor class instead")
            print("INFO     : Instanciation aborted")
            return
        else :
            self._ID        = ID
            self._PortName  = portName #"/dev/ttyACM0"
            self._Baudrate  = CST_BAUDRATE
            
            self._MaxPos    = MOTORS_INFOS_DICT[motor_reference][0]
            self._MaxSpeed  = MOTORS_INFOS_DICT[motor_reference][1]
           
            self._P =   0
            self._I =   0
            self._D =   0
            
            self.start()
        
    """
    Set proportionnal factor
    Return true if correctly changed, else false
    """
    def setP(self, p) -> bool: 
        self._P = p
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, ADDR_P_FACTOR, self._P)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Proportionnal gain modified successfully")

    """
    Set integral factor
    Return true if correctly changed, else false
    """
    def setI(self, i) -> bool: 
        self._I = i
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, ADDR_I_FACTOR, self._I)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Integral gain modified successfully")

    """ 
    Set derivate factor
    Return true if correctly changed, else false
    """
    def setD(self, d) -> bool: 
        self._D = d
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, ADDR_D_FACTOR, self._D)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Derivate gain modified successfully")

    """
    Print all motor information
    Return true if correctly changed, else false
    """
    def showInfo(self) -> bool:
        if (self.getVoltage() == -1) : return False
        if (self.getTemperature() == -1) : return False
        if (self.getLoad() == -1) : return False
        if (self.getPosition() == -1) : return False
        if (self.getSpeed() == -1) : return False

        print("********************MOTOR N°"+str(self._ID)+"********************")
        print("Position 	: ", self._PresentPos)
        print("Vitesse         : ", self._PresentSpeed)
        print("Température	: ", self._Temperature)
        print("Charge 		: ", self._Load)
        print("Voltage         : ", self._Voltage)
        print("Gain P 		: ", self._P)
        print("Gain I 		: ", self._I)
        print("Gain D 		: ", self._D)
        if self._TorqueEnable : print("Couple 		:  Activé") 
        else : print("Couple 		:  Désactivé") 
        print("*******************************************")
        return True

        """
        Return Proportionnal factor
        """
        def getP(self) -> int:
            return self._P

        """
        Return Intergral factor
        """
        def getI(self) -> int:
            return self._I

        """
        Return Derivate factor
        """
        def getD(self) -> int:
            return self._D