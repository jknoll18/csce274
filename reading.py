from interface import Interface
import threading
from threading import Timer
import random
import time
##start
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
  ##this method corresponds to the state of the button, when it pressed initially and beyond that initial pressed
  def isActive2(self):
    ##this variable is needed so that we can create an infinite while loop
    a = 1
    ##Interface().full()
    ##this outer while will allow the program to do an infinite loop
    ##button, 1 being pressed and 0 is not pressed
    while(a == 1): 
      state = 0
      ##this while loop will check when the button is not pressed
      while(state == 0):
        sw = self.readall()
        sw7 = Interface().read_sensor(18) 
        if( sw == 0 and sw7 == 1):
          state = 1
      ##if the state of the button is one it means it the button was pressed
      while(state == 1):
        sw = self.readall()
        sw7 = Interface().read_sensor(18)
        ##if it's pressed then the program will stop
        if( sw7 == 1):
          Interface().stop()
          state = 0
        ##otherwise it will continue to check for the other conditions
        else:
          ##this variable corresponds to the bumper and wheel drop,which is in the interface function
          seven = Interface().read_sensor(7)
          ##this corresponds to the cliff sensors function
          eight = self.readall()
          #the if statement will check if the first element of seven is 1 or the second element of seven is 1
          #this is the one statement we were unable to get it to work. 
          #we tried multiple ways but the song would not play
          if(seven[0] == "1" or  seven[1] == "1"):
            ##Interface().stop()
            Interface().play(0)
            time.sleep(0.125)
            ##print("song")
            ##set to stopped
            state = 0
          ##the timer thread was very convinient for this part because we had practice
          ##using it from the previous project.
          ##this statement will check if any of the cliff sensors are activate
          elif(eight == 1):  ##rotate only
            offset = random.uniform(-0.5,0.5)
            offset2 = float(3 + offset)
            timer0 = Timer(0.0,Interface().drive, args = (100,1))
            timer0.start()
            time.sleep(offset2)
            timer0.cancel()
            ##Interface().stop()
            ##state = 0
          ##this statement will check the left bumper, if it returns a value of 1
          ##then it will rotate 180 for a certain amount of time clockwise, then it will
          ##continue on driving
          elif(seven[3] == "1"): #bumper right cond
            ##rotate cw 180 plus random angle then move forward
            offset = random.uniform(-0.5,0.5)
            offset2 = float(3 + offset)
            timer0 = Timer(0.0,Interface().drive, args = (100,1))
            timer0.start()
            time.sleep(offset2)
            timer0.cancel()
          ##this follows the same logic as the left bumper but it will rotate counterclockwise 
          elif(seven[2] == "1"): ## bumper left cond
            ## rotate ccw 180 plus rand angle then forward
            ##it's a random value from -0.5 to 0.5 because at the 3 seconds it rotates 180 
            ## when we use a velocity of 100, so it's proportial to rotating from a range(+-30) degrees 
            offset = random.uniform(-0.5,0.5)
            offset2 = float(3 + offset)
            timer0 = Timer(0.0,Interface().drive, args = (100,-1))
            timer0.start()
            time.sleep(offset2)
            timer0.cancel()
          ##it will keep on moving if the button was not pressed after the initial press
          else:
            ##move forward
            Interface().drive(100,32768)
  ##this function will read all of the cliff sensors, using the read_sensor function from our interface
  def readall(self):
    sw = Interface().read_sensor(8)
    sw2 = Interface().read_sensor(9)
    sw3 = Interface().read_sensor(10)
    sw4 = Interface().read_sensor(11)
    sw5 = Interface().read_sensor(12)
    sw6 = Interface().read_sensor(13)
    ##if any of the sensors yields 1 then it will return a value of 1
    ##1 being that the sensor was activated
    if( sw == 1 or sw2 == 1 or sw3 == 1 or sw4 == 1 or sw5 == 1 or sw6 == 1):
      return 1
    else:
      return 0

  def wall(self):
    a=1
    while(a==1):
      wall = Interface().read_sensor(45)
      if(wall[5]=="1"):
        Interface().read_sensor(46)
      if(wall[0]== "1"):
        Interface().read_sensor(51)
      if(wall[1]=="1"):
        Interface().read_sensor(50)
      if(wall[2]=="1"):
        Interface().read_sensor(49)
  def pdcontroller(self):
    b = 1
    while(b == 1):
      state = 0
      while (state == 0):
        button = Interface().read_sensor(18)
        if ( button == 1):
          state = 1
      while (state == 1): 
        ##RB signal strength is 40-41
        olderror = 0
        """
        values that worked the best
        kd 1.5,1.3,
        kp 1.5,1.5,
        """ 
        kp = 1.5
        kd = 1.5
        reads = Interface().read_sensor(18)
        if( reads == 1):
          Interface().stop()
          state = 0
        else:
          omni = Interface().read_sensor(17)
          right = Interface().read_sensor(52)
          left = Interface().read_sensor(53)
          if(right== 161 or left ==161 or omni==161):
            self.testIC5()
            state=0
            exit()
            break
          Interface().drive(50,32767) 
          collected = Interface().read_sensor(51)
          collected2 = Interface().read_sensor(45)
          error = collected - 30
          print "error:",error
          pd = (kp*error) + (kd*(error-olderror))
          print pd,"\n"
          olderror = error
          time.sleep(0.60)
          ## this if statement allows the robot to checks if signal 
          ##strength is 0 for the right bumper 
          ## if so then rotate accordingly
          if(collected== 0):
            time0 = Timer(0.0, Interface().drive, args= (125,-200))
            time0.start()
            Interface().close()
            time.sleep(1.5)
            time0.cancel()
          ## if the front right center bumper
          elif( collected2[2]== "1"):
            time2 = Timer(0.0, Interface().drive, args = (100,1))
            time2.start()
            time.sleep(1.5)
            time2.cancel()
          ##this elif statement is when the value of pd is lower than 0
          ## then to adjust the robot using the pd value to go clockwise
          elif(pd <0):
            timer0 = Timer(0.0,Interface().drive, args = (100,-1))
            timer0.start()
            time.sleep(0.1*(abs(pd)/100)) 
            timer0.cancel()
          ##elif is is to check if the pd value is higher than zero 
          ##meaning is going towards the obstacle, when this happens
          ##then adjust it by rotating counter clockwise
          elif(pd > 1):
            timer0 = Timer(0.0,Interface().drive, args = (100,1))
            timer0.start()
            time.sleep(0.6*(abs(pd)/100)) ##was 0.5
            timer0.cancel()
  def testIC3(self):
    a=1
    while(a==1):
      Interface().read_sensor(17)
      Interface().read_sensor(52)
      Interface().read_sensor(53)
  def testIC5(self):
    a=1
    while(a==1):      
      ## -1 is clockwise, 1 is counterclockwise
      dock = Interface().read_sensor(34)
      omni = Interface().read_sensor(17)
      right = Interface().read_sensor(52)
      left = Interface().read_sensor(53)
      if(left == 164 or right == 164 or omni==164):
        Interface().drive(100,-300)
        time.sleep(0.15)
        Interface().stop()
      elif(left == 168 or right == 168 or omni==168):
        Interface().drive(100,300)
        time.sleep(0.15)
        Interface().stop()
      elif(left ==172 or right==172 or omni == 172):
        Interface().drive(75,23767)
        time.sleep(0.20)
        Interface().stop()
      elif(dock[0] == "1"):
        Interface().song()
        Interface().play(1)
        Interface().stop()
        a=2 
