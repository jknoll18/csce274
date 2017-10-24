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
