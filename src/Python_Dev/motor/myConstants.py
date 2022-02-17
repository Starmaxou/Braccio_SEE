#--------------------------------------
#-------------- Generic ---------------
#--------------------------------------
BAUDRATE        = 1000000
PROTOCOL        = 1.0

#--------------------------------------
#--------------- States ---------------
#--------------------------------------
TORQUE_ENABLE   = 1
TORQUE_DISABLE  = 0
LED_ON          = 1
LED_OFF         = 0

MIN_POS         = 0    #relative position, real min = 0 ~ 0°
MAX_POS_NPID    = 1023  #relative position, real max = 1023 ~ 300° 
MAX_POS_PID     = 4092  #relative position, real max = 4095 ~ 360°


#--------------- @12V ---------------
#To calculate max speed value, use motor No Load speed (NLS) parameter : MAX_MOTOR_SPEED = NLS * 1023 / MAX_MOTORSERIE_SPEED (further information on https://emanual.robotis.com/docs/en/dxl/mx/mx-106/#moving-speed)
MIN_SPEED       = 10     
MAX_SPEED_106T  = 394   #relative speed ~ 45 rev/min, each unit equals 0.114 rpm 
MAX_SPEED_64T   = 552   #relative speed ~ 63 rev/min, each unit equals 0.114 rpm
MAX_SPEED_28T   = 482   #relative speed ~ 55 rev/min, each unit equals 0.114 rpm  
MAX_SPEED_AX18A = 870   #relative speed ~ 97 rev/min, each unit equals 0.111 rpm

MOTORS_PID_INFOS_DICT   = {"MX106T": [MAX_POS_PID ,MAX_SPEED_106T] ,"MX64T": [MAX_POS_PID ,MAX_SPEED_64T],"MX28T": [MAX_POS_PID ,MAX_SPEED_28T]}
MOTORS_INFOS_DICT       = {"AX18A": [MAX_POS_NPID, MAX_SPEED_AX18A]}  
MOTORS_INFOS_DICT.update(MOTORS_PID_INFOS_DICT)

#--------------- @12V ---------------
MAX_TORQUE_106T  = 8.4  #N.m @5.2A
MAX_TORQUE_64T   = 6.0  #N.m @4.5A
MAX_TORQUE_28T   = 2.5  #N.m @1.4A
MAX_TORQUE_AX18A = 1.8  #N.m @2.2A

#--------------------------------------
#-------------- Address ---------------
#--------------------------------------
ADDR_TORQUE_ENABLE  = 24
ADDR_LED            = 25
ADDR_D_FACTOR       = 26
ADDR_I_FACTOR       = 27
ADDR_P_FACTOR       = 28
ADDR_GOAL_POS       = 30
ADDR_GOAL_SPEED     = 32
ADDR_TORQUE_LIMIT   = 34
ADDR_PRESENT_POS    = 36
ADDR_PRESENT_SPEED  = 38
ADDR_PRESENT_LOAD   = 40
ADDR_PRESENT_VOLTAGE        = 42
ADDR_PRESENT_TEMPERATURE    = 43

#------------- Board ports ----------------

MOTOR_PORT = 0