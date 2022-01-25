from numpy import unsignedinteger
from DynamixelSDK.python.src import dynamixel_sdk as dxlSdk
from types import *
import myFunctions
import getch
from tokenize import Double

###########################################################################
############################# Global Variable #############################
###########################################################################
#--------------------------------------
#--------------- States ---------------
#--------------------------------------
TORQUE_ENABLE   = 1
TORQUE_DISABLE  = 0
LED_ON          = 1
LED_OFF         = 0

BAUDRATE        = 1000000

#--------------------------------------
#-------------- Address ---------------
#--------------------------------------
ADDR_TORQUE_ENABLE  = 24
ADDR_LED            = 25
ADDR_D_FACTOR       = 26
ADDR_I_FACTOR       = 27
ADDR_P_FACTOR       = 28
ADDR_GOAL_POS       = 30
ADDR_PRESENT_SPEED  = 32
ADDR_PRESENT_POS    = 36
ADDR_PRESENT_LOAD   = 40
ADDR_PRESENT_VOLTAGE        = 42
ADDR_PRESENT_TEMPERATURE    = 43
###########################################################################
###########################################################################

class Motor :
    _Protocol       = 1.0
    _Baudrate       = 1000000
    _Error          = 0
    
    _MinPos	        = 0
    _MaxPos	        = 1023
    _MaxSpeed       = 1023

    _GoalPos        = 0
    _Speed	        = 300           
    _TorqueEnable   = TORQUE_ENABLE
    _Led            = LED_OFF
    
    _Threshold      = 8
        
    def __init__(self, ID, portName, CST_BAUDRATE) -> None:
        self._ID        = ID
        self._PortName  = portName #"/dev/ttyACM0"
        self._Baudrate  = CST_BAUDRATE
        
        self.start()
        
    """
    Starting motor routine
    """
    def start(self) -> bool:
        """
        Initializes PortHandler instance
        Sets the port path
        Gets methods and members of PortHandlerLinux or PortHandlerWindows
        """
        self._portHandler = dxlSdk.PortHandler(self._PortName)

        """
        Initializes PacketHandler instance
        Sets the protocol version
        Gets methods and members of Protocol1PacketHandler or Protocol2PacketHandler
        """
        self._packetHandler = dxlSdk.PacketHandler(self._Protocol)

        #Open port
        if(not(self.openPort())):
            return False
        
        #Set port baudrate
        if(not(self.setBaudrate(self._Baudrate))):
            return False
        
        #Enable torque
        if (not(self.enableTorque())):
            return False

        #Set speed
        if (not(self.setSpeed(self._Speed))):
            return False
        
        #Get initial voltage, temperature and load
        if (self.getVoltage() == -1):
            return False
        if (self.getTemperature() == -1):
            return False
        if (self.getLoad() == -1):
            return False
        
        print("Motor n°"+ self._ID + " correctly started.")
        return True
    
    """
    Open the USB port
    @return True if correctly opened, else False
    """
    def openPort(self) -> bool:
        if (self._portHandler.openPort()):
            print("Succeeded to open the port")
            return True
        else :
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            return False

    """
    Change the baudrate
    @param baudrate : New baudrate
    @return True if the baudrate is correctly changed, else False
    """
    def setBaudrate(self, baudrate) -> bool:
        if (self._portHandler.setBaudRate(baudrate)):
            print("Succeeded to change the baudrate")
            return True
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            return False

    """
    Enable motor torque
    @return True if correctly enabled, else False
    """
    def enableTorque(self) -> bool : 
        self._TorqueEnable = TORQUE_ENABLE
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, ADDR_TORQUE_ENABLE, self._TorqueEnable)
        
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Torque enabled successfully")
    
    """
    Disable motor torque
    @return True if correctly enabled, else False
    """
    def disableTorque(self) -> bool : 
        self._TorqueEnable = TORQUE_DISABLE
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, ADDR_TORQUE_ENABLE, self._TorqueEnable)
        
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Torque enabled successfully")
    
    """
    Modify the velocity
    @param speed New velocity
    @return True if correctly modified, else False
    """
    def setSpeed(self, targetSpeed) -> bool :
        self._Speed = targetSpeed if (targetSpeed < self._MaxSpeed) else self._MaxSpeed
        self._ComResult, self._Error = self._packetHandler.write2ByteTxRx(self._portHandler, self._ID, ADDR_PRESENT_SPEED, self._Speed)
        
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Velocity modified successfully")
        
    """
    Recover the motor voltage
    @return motor voltage, -1 if communication didn't worked
    """
    def getVoltage(self) -> Double:
        Voltage, self._ComResult, self._Error  = self._packetHandler.read1ByteTxRx(self._portHandler, self._ID, ADDR_PRESENT_VOLTAGE)
        
        if self.verifComm(self._packetHandler, self._ComResult, self._Error, "Voltage recovered successfully") : 
            self._Voltage = Voltage / 10
            return self._Voltage
        else :
            return -1
        
    """
    Recover the motor temperature
    @return motor temperature, -1 if communication didn't worked
    """
    def getTemperature(self) -> Double:
        self._Temperature, self._ComResult, self._Error  = self._packetHandler.read1ByteTxRx(self._portHandler, self._ID, ADDR_PRESENT_TEMPERATURE)
        
        if self.verifComm(self._packetHandler, self._ComResult, self._Error, "Temperature recovered successfully") : 
            return self._Temperature
        else :
            return -1
    
    """
    Recover the motor load
    @return motor load, -1 if communication didn't worked
    """
    def getLoad(self) -> Double:
        Load, self._ComResult, self._Error  = self._packetHandler.read2ByteTxRx(self._portHandler, self._ID, ADDR_PRESENT_LOAD)
        
        if self.verifComm(self._packetHandler, self._ComResult, self._Error, "Load recovered successfully") : 
            if (Load > 2047) : Load = 2047
            if (Load < 1024) : 
                print("The motor is loaded counter clock wise")
            elif (Load >= 1024) : 
                print("The motor is loaded clock wise")
                Load -= 1024
            self._Load = Load * 100 / 1024
            return self._Load
        else :
            return -1

    """
    Recover the motor position
    @return motor position, -1 if communication didn't worked
    """
    def getPosition(self) -> unsignedinteger:
        self._PresentPos, self._ComResult, self._Error  = self._packetHandler.read2ByteTxRx(self._portHandler, self._ID, ADDR_PRESENT_POS)
        
        if self.verifComm(self._packetHandler, self._ComResult, self._Error, "Load recovered successfully") : 
            return self._PresentPos
        else :
            return -1
    
    """
    Move motor
    @param newPos New position of the motor
    @param isDegree Indicates if the position is given in degree
    @param isBlocking Should the movment be blocking ? (False by default)
    @returns true if moved correctly, else false
    """
    def move(self, newPos : unsignedinteger, isDegree : bool, isBlocking : bool, debug : bool) -> bool :
        if isDegree :
            self._GoalPos = myFunctions.mapping(newPos, 0, 360, self._MinPos, self._MaxPos)
        else :
            self._GoalPos = newPos % self._MaxPos
            
        #Write goal position
        self._ComResult, self._Error = self._packetHandler.write2ByteTxRx(self._portHandler, self._ID, ADDR_GOAL_POS, self._GoalPos)
        self.verifComm(self._packetHandler, self._ComResult, self._Error, "")
        
        if isBlocking :
            while True :
                self._PresentPos, self._ComResult, self._Error  = self._packetHandler.read2ByteTxRx(self._portHandler, self._ID, ADDR_PRESENT_POS)
                self.verifComm(self._packetHandler, self._ComResult, self._Error, "")
                				
                if debug : print("[ID: "+ self._ID + "] GoalPos:"+ self._GoalPos+ " - PresPos: "+ self._PresentPos)
                
                if (self._PresentPos < self._MinPos) : self._PresentPos = self._MinPos
                if (self._PresentPos > self._MaxPos) : self._PresentPos = self._MaxPos
                
                dif = self._GoalPos - self._PresentPos
                
                if abs(dif) <= self._Threshold : break
        
        return True        

    """
    Turn off motor led
    Return true if correctly changed, else false
    """
    def ledOff(self) -> bool:
        self._Led = LED_OFF
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, ADDR_LED, self._Led)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Led turned off successfully")
    
    """
    Turn on motor led 
    Return true if correctly changed, else false
    """
    def ledOn(self) -> bool:
        self._Led = LED_ON
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, ADDR_LED, self._Led)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Led turned on successfully")

    """
    Return current motor baudrate   
    """
    def getBaudrate(self) -> unsignedinteger:      
        return self._Baudrate
 
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
        if self._TorqueEnable : print("Couple 		: Activé") 
        else : print("Couple 		: Désactivé") 
        print("Vitesse 	    : ",self._Speed)
        print("*********************************")
        return True

    def closePort(self) :
        self._portHandler.closePort()

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

