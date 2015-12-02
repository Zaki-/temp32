ID=api.GetServoValue()
moveToValue = 0
if moveToValue > ID:
  if delay<=ID:
    steps=int((moveToValue-ID)/delay)
    while i<delay :
      delay=delay +1
    
