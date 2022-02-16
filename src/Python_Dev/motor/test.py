import time
import myFunctions

############ Servos ###########
PresentPos = 0
############ VAR ##############
TTR     = 10
TTA     = 1
InPos = 355
###############################

GoalPos = myFunctions.mapping(InPos, 0, 360, 0, 4092)

V2 = round(abs(GoalPos - PresentPos) / (TTR-TTA))   #Constant speed to reach 

nbStep      = 10                                    #Number of steps when accelerating
stepSpeed   = round(V2 / nbStep)                    #Speed step value 
stepTime    = TTA / nbStep                   #Time step value

print("**********************************************")
print("DELTA POS : ",GoalPos, ", TTA : ", TTA, ", TTR :", TTR)
print("V2 : ", V2,", STEP TIME : ", stepTime, ", STEP SPEED : ", stepSpeed)
print("**********************************************")


##Set initial speed
#self._GoalSpeed = MIN_SPEED
GoalSpeed = 0

##Write speed position
#self.setSpeed() 

##Write goal position
#self.setGoalPosition() 


#----------Acceleration----------
print("--------------------------------\n",
        "----------Acceleration----------\n",
        "--------------------------------")

start_time = time.time()
actualTime = start_time

i = 1
print("~~~~~~~~~~Step n°", i, "~~~~~~~~~~" )
print("\tActualTime : ", actualTime)
print("\tGoalSpeed : ", GoalSpeed, "\n")
            
i = 1
while(i < nbStep + 1):
    actualTime = time.time() - start_time
    
    if (actualTime >= (i * stepTime)):
        print("~~~~~~~~~~Step n°", i, "~~~~~~~~~~" )
        print("\tActualTime : ", actualTime)
        print("\tGoalSpeed : ", GoalSpeed, "\n")

        GoalSpeed += stepSpeed
       
        i+=1
        print("~~~~~~~~~~Step n°", i, "~~~~~~~~~~" )
        print("\tActualTime : ", actualTime)
        print("\tGoalSpeed : ", GoalSpeed, "\n")
        #self.setSpeed()
        

#----------Croisiere----------
while((time.time()- start_time) <= (TTR - TTA)):
    pass

#----------Decceleration----------
i = 1
while(i < nbStep + 1):
    actualTime = time.time() - start_time
    
    if (actualTime >= ((i * stepTime)+TTR-TTA)):

        GoalSpeed -= stepSpeed
        i+=1
        print("~~~~~~~~~~Step n°", i, "~~~~~~~~~~" )
        print("\tActualTime : ", actualTime)
        print("\tGoalSpeed : ", GoalSpeed)
        #self.setSpeed()