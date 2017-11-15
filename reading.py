from interface import Interface
from threading import Timer
import random
import time
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
    a = 1
    ##Interface().full()
    while(a == 1):
      state = 0
      while(state == 0):
        sw = self.readall()
        sw7 = Interface().read_sensor(18)
        if( sw == 0 and sw7 == 1):
          state = 1
      while(state == 1):
        sw = self.readall()
        sw7 = Interface().read_sensor(18)
        
        if( sw7 == 1):
          Interface().stop()
          state = 0
        else:
          LightBump = Interface().read_sensor(45)
          seven = Interface().read_sensor(7)
          eight = self.readall()
          if(seven[0] == "1" or  seven[1] == "1"):
            ## Interface().song()
            Interface().play(0)
            time.sleep(5)
            Interface().stop()
            ##set to stopped
            state = 0
          elif(eight == 1):  ##rotate only
            offset = random.uniform(-0.5,0.5)
            offset2 = float(3 + offset)
            timer0 = Timer(0.0,Interface().drive, args = (100,1))
            timer0.start()
            time.sleep(offset2)
            timer0.cancel()
            ##Interface().stop()
            ##state = 0
          elif(seven[3] == "1"): #bumper right cond
            ##rotate cw 180 plus random angle then move forward
            offset = random.uniform(-0.5,0.5)
            offset2 = float(3 + offset)
            timer0 = Timer(0.0,Interface().drive, args = (100,1))
            timer0.start()
            time.sleep(offset2)
            timer0.cancel()
          elif(seven[2] == "1"): ## bumper left cond
            ## rotate ccw 180 plus rand angle then forward
            offset = random.uniform(-0.5,0.5)
            offset2 = float(3 + offset)
            timer0 = Timer(0.0,Interface().drive, args = (100,-1))
            timer0.start()
            time.sleep(offset2)
            timer0.cancel()
         


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
    if( sw == 1 or sw2 == 1 or sw3 == 1 or sw4 == 1 or sw5 == 1 or sw6 == 1):
      return 1
    else:
      return 0
  ##function for project 3  
  ##this wall function was used to see observe wall values 
  ##were obtained when it come in close proximity of a wall  
  def wall(self):
     a=1
     ##this is an infinite while loop that constaintly look for the signal 
     ##strength when one of the bits in sensor 45 was activated
     while(a==1):
       ##for each bit activated(turns value to 1) the proper sensor
       ##will be activated
       wall = Interface().read_sensor(45)
       if(wall[5]=="1"):
         Interface().read_sensor(46)
       if(wall[0]=="1"):
         Interface().read_sensor(51)
       if(wall[1]=="1"):
         Interface().read_sensor(50)
       if(wall[2]=="1"):
         Interface().read_sensor(49)
       if(wall[3]=="1"):
         Interface().read_sensor(48)
       if(wall[4]=="1"):
         Interface().read_sensor(47)
  def pdcontroller(self):
     ##RB signal strength is 40-41
     ##this is the intial error when the robot is activated for the first time
     olderror = 0
     """
     values that worked the best
     kd 1.5,1.3,
     kp 1.5,1.5,
     """
     kp = 1.5
     kd = 1.5
     run = 1
     ##timer3 = Timer(0.0,Interface().drive, args=(50,32767))
     ##timer3.start()
     ##this is also an infinite loop that way it's constaintly 
     ##updating the values for the pd controller 
     while(run == 1):
       Interface().drive(50,32768)
       collected = Interface().read_sensor(51)
       error = collected - 30
       ##this was used to observe what values were obtain when subtracted
       ##with the targeted value
       print "error:",error
       pd = (kp*error) + (kd*(error-olderror))
       print pd,"\n"
       olderror = error
       time.sleep(0.5)
       if(pd <0):
         timer0 = Timer(0.0,Interface().drive, args = (100,-1))
         timer0.start()
         time.sleep(0.5*(abs(pd)/100))
         timer0.cancel()
       if(pd >1):
         timer0 = Timer(0.0,Interface().drive, args = (100,1))
         timer0.start()
         time.sleep(abs(pd)/100)
         timer0.cancel()     

