from tokenize import Double
from xmlrpc.client import boolean
from DynamixelSDK.python.tests.protocol1_0.read_write import TORQUE_DISABLE, TORQUE_ENABLE
from Motor import *

class MX12W(Motor) :

    _TorqueEnableAddr   = 24
    _LedAddr			= 25
    _DAddr				= 26
    _IAddr				= 27
    _PAddr				= 28
    _GoalPosAddr    	= 30
    _SpeedAddr			= 32
    _PresentPosAddr 	= 36
    _LoadAddr			= 40
    _VoltageAddr		= 42
    _TemperatureAddr	= 43

    _Protocol       	= 1.0

    _MinPos				= 0
    _MaxPos				= 4095
    _MaxSpeed           = 300
    _Speed				= 300
    _TorqueEnable   	= TORQUE_ENABLE
    _Led                = LED_ON

    def __init__(self, ID) -> None:
        super().__init__(ID)
        self.start()
    
    def start(self) -> boolean:
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
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, self._TorqueEnableAddr, self._TorqueEnable)
        
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Torque enabled successfully")
    
    """
    Disable motor torque
    @return True if correctly enabled, else False
    """
    def disableTorque(self) -> bool : 
        self._TorqueEnable = TORQUE_DISABLE
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, self._TorqueEnableAddr, self._TorqueEnable)
        
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Torque enabled successfully")
    
    """
    Modify the velocity
    @param speed New velocity
    @return True if correctly modified, else False
    """
    def setSpeed(self, targetSpeed) -> bool :
        self._Speed = targetSpeed if (targetSpeed < self._MaxSpeed) else self._MaxSpeed
        self._ComResult, self._Error = self._packetHandler.write2ByteTxRx(self._portHandler, self._ID, self._SpeedAddr, self._Speed)
        
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Velocity modified successfully")
        
    """
    Recover the motor voltage
    @return motor voltage, -1 if communication didn't worked
    """
    def getVoltage(self) -> Double:
        Voltage, self._ComResult, self._Error  = self._packetHandler.read1ByteTxRx(self._portHandler, self._ID, self._VoltageAddr)
        
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
        self._Temperature, self._ComResult, self._Error  = self._packetHandler.read1ByteTxRx(self._portHandler, self._ID, self._TemperatureAddr)
        
        if self.verifComm(self._packetHandler, self._ComResult, self._Error, "Temperature recovered successfully") : 
            return self._Temperature
        else :
            return -1
    
    """
    Recover the motor load
    @return motor load, -1 if communication didn't worked
    """
    def getLoad(self) -> Double:
        Load, self._ComResult, self._Error  = self._packetHandler.read2ByteTxRx(self._portHandler, self._ID, self._LoadAddr)
        
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
        self._PresentPos, self._ComResult, self._Error  = self._packetHandler.read2ByteTxRx(self._portHandler, self._ID, self._PresentPosAddr)
        
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
        self._ComResult, self._Error = self._packetHandler.write2ByteTxRx(self._portHandler, self._ID, self._GoalPosAddr, self._GoalPos)
        self.verifComm(self._packetHandler, self._ComResult, self._Error, "")
        
        if isBlocking :
            while True :
                self._PresentPos, self._ComResult, self._Error  = self._packetHandler.read2ByteTxRx(self._portHandler, self._ID, self._PresentPosAddr)
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
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, self._LedAddr, self._Led)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Led turned off successfully")
    
    """
    Turn on motor led 
    Return true if correctly changed, else false
    """
    def ledOn(self) -> bool:
        self._Led = LED_ON
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, self._LedAddr, self._Led)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Led turned on successfully")
    
    """
    Set proportionnal factor
    Return true if correctly changed, else false
    """
    def setP(self, p) -> bool: 
        self._P = p
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, self._PAddr, self._P)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Proportionnal gain modified successfully")

    """
    Set integral factor
    Return true if correctly changed, else false
    """
    def setI(self, i) -> bool: 
        self._I = i
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, self._IAddr, self._I)
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Integral gain modified successfully")

    """ 
    Set derivate factor
    Return true if correctly changed, else false
    """
    def setD(self, d) -> bool: 
        self._D = d
        self._ComResult, self._Error = self._packetHandler.write1ByteTxRx(self._portHandler, self._ID, self._DAddr, self._D)
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
    
    def closePort(self) :
	    self._portHandler.closePort()