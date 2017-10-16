from interface import Interface
from threading import Timer
class Reading: 
  def __init__(self):
    press = False
  def isActive(self):
    count = 0
    state = 1
    while count < 5:
      sw = Interface().read_sensor(18)
      if sw == 1:
        state += 1
        if state % 2 == 0:
          Interface().penta()
          count += 1
        else:
          Interface().stop
      if sw == 0:
        if state % 2 == 0:
          Interface().penta()
          count += 1
        else:
          Interface().stop
  def isActive2(self):
    state = 0
	while(state == 0):
      sw = self.readall()
	  sw7 = Interface().read_sensor(18)
	  if( sw == 1 and sw7 == 1):
	    state = 1
    while(state == 1):
      sw = self.readall()
	  sw7 = Interface().read_sensor(18)
	  if( sw7 == 1):
	    Interface().stop()
        seven = Interface().read_sensor(7)
		s3 = seven[2]
		s4 = seven[3]
		if( s3 or s4 == "1"):
		  Interface().play()
          state = 0
	  else:
	    seven = Interface().read_sensor(7)
		eight = self.readall()
		if(seven[2] == "1" or seven[3] == "1"):
		  ##stop
		  ##set to stopped
		if(seven[0] == "1" or seven[1] == '1'or eight == 1):
		  ##rotate only
		if(seven[0] == "1"): #bumper right cond
		  ##rotate cw 180 plus random angle then move forward
		  Interface().drive(100,1)
		  Interface().drive(100,32768)
		elif(seven[1] == "1"): ## bumper left cond
		  ## rotate ccw 180 plus rand angle then forward
		  Interface().drive(100,-1)
		  Interface().drive(100,32768)
		else:
		  ##move forward
		  Interface().drive(100,32768)
  def readall(self):
    sw = Interface().read_sensor(8)
    sw2 = Interface().read_sensor(9)
    sw3 = Interface().read_sensor(10)
    sw4 = Interface().read_sensor(11)
    sw5 = Interface().read_sensor(12)
    sw6 = Interface().read_sensor(13)
    if( sw or sw2 or sw3 or sw4 or sw5 or sw6 == 1):
      return 1
    else:
      return 0