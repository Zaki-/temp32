from time import sleep

# To control single servo 
def SingleMotor(ID, POS, TIME): 
#ID: servo ID - POS: the target position - TIME:the time it takes for the servo to go to the target position POS max is 5sec
  if (ID>=1) and (ID<=20) and (POS>=1) and (POS<=1024) and (TIME>0) and (TIME<=5):
    OldPos=api.GetMotorValue() #read the current servo position
    DIS = abs(POS-OldPos) 
    StepDelay=TIME/DIS
    for i in range(OldPos,POS):
      api.SetMotorValue(i)
      sleep(StepDelay)    
