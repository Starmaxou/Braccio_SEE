from Motor import *

class MotorPID(Motor) :
 
    def __init__(self, ID, portName, CST_BAUDRATE) -> None:
        super().__init__(ID, portName, CST_BAUDRATE)
        
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

        print("*********************************")
        print("Position 	: ", self._PresentPos)
        print("Température	: ", self._Temperature)
        print("Charge 		: ", self._Load)
        print("Voltage 	    : ", self._Voltage)
        print("Gain P 		: ", self._P)
        print("Gain I 		: ", self._I)
        print("Gain D 		: ", self._D)
        if self._TorqueEnable : print("Couple 		: Activé") 
        else : print("Couple 		: Désactivé") 
        print("Vitesse 	    : ",self._Speed)
        print("*********************************")
        return True
