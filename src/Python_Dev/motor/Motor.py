from markupsafe import string
from numpy import int
from motor.DynamixelSDK.python.src import dynamixel_sdk as dxlSdk
from types import *
import getch
from tokenize import Double
import time

import motor.myFunctions
from motor.myConstants import *


class Motor :

    #Init values   
    _Error          = 0
    _Moving         = False

    _MinPos         = MIN_POS
    _MinSpeed       = MIN_SPEED
    _GoalPos        = 0
    _GoalSpeed      = 300           
    _TorqueEnable   = TORQUE_ENABLE
    _Led            = LED_OFF
    
    _Threshold      = 8
        
    def __init__(self, motor_reference : string , ID : int, portName : string , CST_BAUDRATE : int) -> None:
        if not(motor_reference in MOTORS_INFOS_DICT) :
            print("ERROR    : Motor reference unknown. This class can only handle Dynamixel MX160T, MX64T, MX28T and AX18A")
            print("INFO     : Instanciation aborted")
            return
        elif motor_reference in MOTORS_PID_INFOS_DICT :
            print("WARNING  : You are trying to instanciate a class not corresponding to your motor, use Motor PID class instead")
            print("INFO     : Instanciation aborted")
            return
        else :
            self._ID        = ID
            self._PortName  = portName #"/dev/ttyACM0"
            self._Baudrate  = CST_BAUDRATE
            
            self._MaxPos    = MOTORS_INFOS_DICT[motor_reference][0]
            self._MaxSpeed  = MOTORS_INFOS_DICT[motor_reference][1]
            print("Constr OK")
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
        print("portHadler OK")

        """
        Initializes PacketHandler instance
        Sets the protocol version
        Gets methods and members of Protocol1PacketHandler or Protocol2PacketHandler
        """
        self._packetHandler = dxlSdk.PacketHandler(PROTOCOL)
        print("packetHandler OK")

        #Open port
        self.openPort()
                
        #Set port baudrate
        self.setBaudrate(self._Baudrate)

        #Enable torque
        self.enableTorque()

        #Set speed
        self.setSpeed()        
        
        #Get initial voltage, temperature and load
        self.getVoltage() 
        self.getTemperature()
        self.getLoad() 
        
        
        self.showInfo()
        print("Motor n°"+ str(self._ID) + " correctly started.")
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
    Modify the goal position
    @return True if correctly modified, else False
    """
    def setGoalPosition(self) -> bool :
        self._GoalPos = self._GoalPos if (self._GoalPos < self._MaxPos) else self._MaxPos
        self._ComResult, self._Error = self._packetHandler.write2ByteTxRx(self._portHandler, self._ID, ADDR_GOAL_POS, self._GoalPos)
        
        return self.verifComm(self._packetHandler, self._ComResult, self._Error, "Goal Position modified successfully")
        
    """
    Modify the velocity
    @return True if correctly modified, else False
    """
    def setSpeed(self) -> bool :
        self._GoalSpeed = self._GoalSpeed if (self._GoalSpeed < self._MaxSpeed) else self._MaxSpeed
        self._ComResult, self._Error = self._packetHandler.write2ByteTxRx(self._portHandler, self._ID, ADDR_GOAL_SPEED, self._GoalSpeed)
        
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
                print("The motor is loaded clock wise")
                self._Load = Load * 100 / 1024

            elif (Load >= 1024) : 
                print("The motor is loaded counter clock wise")
                Load -= 1024
                self._Load = Load * -100 / 1024
            return self._Load
        else :
            return -1

    """
    Recover the motor position
    @return motor position, -1 if communication didn't worked
    """
    def getPosition(self) -> int:
        self._PresentPos, self._ComResult, self._Error  = self._packetHandler.read2ByteTxRx(self._portHandler, self._ID, ADDR_PRESENT_POS)
 
        if self.verifComm(self._packetHandler, self._ComResult, self._Error, "Position recovered successfully") : 
            return self._PresentPos
        else :
            return -1
    
    """
    Recover the motor speed
    @return motor speed, -1 if communication didn't worked
    """
    def getSpeed(self) -> int:
        self._PresentSpeed, self._ComResult, self._Error  = self._packetHandler.read2ByteTxRx(self._portHandler, self._ID, ADDR_PRESENT_SPEED)
 
        if self.verifComm(self._packetHandler, self._ComResult, self._Error, "Speed recovered successfully") : 
            return self._PresentSpeed
        else :
            return -1
        
    
    """
    Move motor
    @param newPos New position of the motor
    @param isDegree Indicates if the position is given in degree
    @param isBlocking Should the movment be blocking ? (False by default)
    @returns true if moved correctly, else false
    """
    def move(self, newPos : int, TTR = -1, isDegree = False) -> bool :
        #------Convert degree in relative postiion------
        if isDegree :
            if self._MaxPos == MAX_POS_NPID :
                self._GoalPos = myFunctions.mapping(newPos, 0, 300, self._MinPos, self._MaxPos)
            else : 
                self._GoalPos = myFunctions.mapping(newPos, 0, 360, self._MinPos, self._MaxPos)
        else :
            self._GoalPos = newPos % self._MaxPos
        
        TTA = 0.25 * TTR
        
        self.getPosition()  
        
        nbStep      = 30                                    #Number of steps when accelerating

        
        if TTR == -1 : #Pour la commande via les oeufs
            TTR = 2
            TTA = 0.25
            
            V2 = round(abs(self._GoalPos - self._PresentPos) / ((TTR-TTA)*10))   #Constant speed to reach 
            stepSpeed   = round(V2 / nbStep)                    #Speed step value 
            stepTime    = TTA / nbStep                          #Time step value
            
            print("**********************************************")
            print("GOAL POS - PRESENT POS = DELTA POS : \t", self._GoalPos," - ", self._PresentPos," = abs(", abs(self._GoalPos - self._PresentPos),")\n",
                "TTA : ", TTA, ", TTR :", TTR," V2 : ", V2,", STEP TIME : ", stepTime, ", STEP SPEED : ", stepSpeed)
            print("**********************************************")

        else :  
        
            V2 = round(abs(self._GoalPos - self._PresentPos) / ((TTR-TTA)*10))   #Constant speed to reach 
            self.AccelerationMovement(V2, TTR, TTA, nbStep)
        
        self.getPosition()
        
        """
        print("************************************\n",
                "Erreur de position : ", abs(self._PresentPos - self._GoalPos),"\n",
                "************************************\n",
                )
        """
                    
        return True      
    
    """
    Acceleration
    """  
    def AccelerationMovement(self, V, TTR, TTA, nbStep):
        stepSpeed   = round(V / nbStep)                    #Speed step value 
        stepTime    = TTA / nbStep                          #Time step value
        
        """
        print("**********************************************")
        print("GOAL POS - PRESENT POS = DELTA POS : \t", self._GoalPos," - ", self._PresentPos," = abs(", abs(self._GoalPos - self._PresentPos),")\n",
            "TTA : ", TTA, ", TTR :", TTR," V : ", V,", STEP TIME : ", stepTime, ", STEP SPEED : ", stepSpeed)
        print("**********************************************")
        """
        
        
        ##Set initial speed
        self._GoalSpeed = MIN_SPEED
        
        ##Write speed position
        self.setSpeed() 

        ##Write goal position
        self.setGoalPosition() 

        """
        #----------Acceleration----------
        print("--------------------------------\n",
                "----------Acceleration----------\n",
                "--------------------------------")
        """
        
        start_time = time.time()
        actualTime = start_time
        
        i = 1
        
        """
        print("~~~~~~~~~~Step n°", i, "~~~~~~~~~~" )
        print("\tActualTime : ", actualTime)
        print("\tGoalSpeed : ", self._GoalSpeed, "\n")
        """
        
        while(i < nbStep + 1):
            actualTime = time.time() - start_time
            
            if (actualTime >= (i * stepTime)):
                
                self._GoalSpeed += stepSpeed
                
                if self._GoalSpeed > self._MaxSpeed : self._GoalSpeed = self._MaxSpeed
                if self._GoalSpeed < self._MinSpeed : self._GoalSpeed = self._MinSpeed
            
                i+=1
                """
                print("~~~~~~~~~~Step n°", i, "~~~~~~~~~~" )
                print("\tActualTime : ", actualTime)
                print("\tGoalSpeed : ", self._GoalSpeed)
                """
                self.setSpeed()
                #print()
            
                
        """
        #----------Croisiere----------
        print("--------------------------------\n",
                "------------Croisière-----------\n",
                "--------------------------------\n")
                
        print("\tActualTime : ", actualTime)
        """
        while((time.time()- start_time) <= ( (TTR - TTA))):
            pass
        
        

        #----------Decceleration----------
        """
        print("--------------------------------\n",
                "----------Decceleration---------\n",
                "--------------------------------")
        """
        
        i = 1
        actualTime = time.time()
        
        """
        print("~~~~~~~~~~Step n°", i, "~~~~~~~~~~" )
        print("\tActualTime : ", actualTime)
        print("\tGoalSpeed : ", self._GoalSpeed, "\n")
        """
        
        while(i < nbStep + 1):
            actualTime = time.time() - start_time
            
            if (actualTime >= ((i * stepTime)+TTR-TTA)):

                self._GoalSpeed -= stepSpeed
                
                if self._GoalSpeed < 0 : self._GoalSpeed = self._MinSpeed
                if self._GoalSpeed < self._MinSpeed : self._GoalSpeed = self._MinSpeed

                i+=1
                
                """
                print("~~~~~~~~~~Step n°", i, "~~~~~~~~~~" )
                print("\tActualTime : ", actualTime)
                print("\tGoalSpeed : ", self._GoalSpeed)
                """
                self.setSpeed()
                #print()     
        

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
    def getBaudrate(self) -> int:      
        return self._Baudrate
 
    """
    Return motor maximum speed
    """
    def getMaxSpeed(self) -> int:
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
        if (CommunicationResult != dxlSdk.COMM_SUCCESS) :
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
        if (self.getSpeed() == -1) : return False
        if (self.getPosition() == -1) : return False
        
        print("********************MOTOR N°"+str(self._ID)+"********************")
        print("Position 	: ", self._PresentPos)
        print("Vitesse         : ", self._PresentSpeed)
        print("Température	: ", self._Temperature)
        print("Charge 		: ", self._Load)
        print("Voltage         : ", self._Voltage)
        if self._TorqueEnable : print("Couple 		:  Activé") 
        else : print("Couple 		:  Désactivé") 
        print("*********************************")
        return True

    """
    Properly close portHandler
    """
    def closePort(self) :
        self._portHandler.closePort()
