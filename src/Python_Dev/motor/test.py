import time

############ Servos ###########
PresentPos = 0
############ VAR ##############
TTR     = 10
TTA     = 1
GoalPos = 2000
###############################


V2 = round(abs(GoalPos - PresentPos) / (TTR-TTA))   #Constant speed to reach 

nbStep      = 10                                    #Number of steps when accelerating
stepSpeed   = round(V2 / nbStep)                    #Speed step value 
stepTime    = TTA / nbStep                   #Time step value

print("V2 : ", V2,", STEP TIME : ", stepTime, ", STEP SPEED : ", stepSpeed)

##Set initial speed
#self._GoalSpeed = MIN_SPEED
GoalSpeed = 0

##Write speed position
#self.setSpeed() 

##Write goal position
#self.setGoalPosition() 


#----------Acceleration----------
start_time = time.time()

i = 1
while(i < nbStep + 1):
    actualTime = time.time() - start_time
    
    if (actualTime >= (i * stepTime)):
        print("ActualTime : ", actualTime)

        GoalSpeed += stepSpeed
        print("GoalSpeed : ", GoalSpeed)
        i+=1
        print("NEXT STEP : ", i * stepTime)
        #self.setSpeed()
        

#----------Croisiere----------
while((time.time()- start_time) <= (TTR - TTA)):
    pass

#----------Decceleration----------
i = 1
while(i < nbStep + 1):
    actualTime = time.time() - start_time
    
    if (actualTime >= ((i * stepTime)+TTR-TTA)):
        print("ActualTime : ", actualTime)

        GoalSpeed -= stepSpeed
        print("GoalSpeed : ", GoalSpeed)
        i+=1
        print("NEXT STEP : ", i * stepTime)
        #self.setSpeed()