from numpy import unsignedinteger
from DynamixelSDK.python.src import dynamixel_sdk as dxlSdk
from types import *
import myFunctions
import getch

from DynamixelSDK.python.tests.protocol1_0.read_write import TORQUE_DISABLE

TORQUE_ENABLE   = 1
TORQUE_DISABLE  = 0

class Motor :
    
    _P = 0
    _I = 0
    _D = 0
        
    def __init__(self, ID) -> None:
        self._ID = ID
        self._PortName = "/dev/ttyACM0"
        
        self._Baudrate   = 1000000  
        self._MaxSpeed   = 1023
        self._Threshold  = 8
        self._GoalPos    = 0   
        self._Error      = 0
    
    """
    Return current motor baudrate   
    """
    def getBaudrate(self) -> unsignedinteger:      
        return self._Baudrate

    """
    Return Proportionnal factor
    """
    def getP(self) -> unsignedinteger:
        return self._P
    
    """
    Return Intergral factor
    """
    def getI(self) -> unsignedinteger:
        return self._I
    
    """
    Return Derivate factor
    """
    def getD(self) -> unsignedinteger:
        return self._D
 
    """
    Return current motor speed
    """
    def getSpeed(self) -> unsignedinteger:
        return self._Speed
    
    """
    Return motor maximum speed
    """
    def getMaxSpeed(self) -> unsignedinteger:
        return self._MaxSpeed
    
    """
    Return state of torque (enabled/disabled)
    """
    def getTorque(self) -> bool:
        return self._TorqueEnable
    
    """
    Turn off motor led
    return LED state 
    """
    def ledOff(self) -> bool:
        self._Led = False
        return self._Led
    
    """
    Turn on motor led 
    return LED state
    """
    def ledOn(self) -> bool:
        self._Led = True
        return self._Led
    
    """
    Set proportionnal factor
    """
    def setP(self) -> bool:
        ###########################################################
        ####################### TO DO #############################
        ###########################################################
        pass
        
    """
    Set integral factor
    """
    def setI(self) -> bool:
        ###########################################################
        ####################### TO DO #############################
        ###########################################################
        pass
    
    """
    Set derivate factor
    """
    def setD(self) -> bool:
        ###########################################################
        ####################### TO DO #############################
        ###########################################################
        pass
    
    """
    Verify the communication status 
    """
    def verifComm(self, packetHandler : dxlSdk.Protocol1PacketHandler, CommunicationResult, Error, strSuccess) -> bool:
        if (strSuccess != dxlSdk.COMM_SUCCESS) :
            print("%s" % packetHandler.getTxRxResult(CommunicationResult))
            return False
        elif self._Error != 0:
            print("%s" % packetHandler.getRxPacketError(Error))
            return False
        else:
            print(strSuccess)
            return True