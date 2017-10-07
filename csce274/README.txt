interface.py

this file contains the interface that combines the tasks of part 1 and 2. 
writing and sending commands to the machine
process then close information
start
reset : def reset(self):  ##the reset function to reset the robot and put it into passive
stop : def stop(self):  ##the stop function to the robot
passive : def passive(self):  ##the passive function reconnects the robot to the original passive state
safe : def safe(self):  ##the safe function sets the robot to the state safe

drive command : def drive(self,velocity,radius): ## drive function
Pentagon Drive command : def penta(self) : this allows the robot to move in a pentagon formation
main.py

instructions for connecting to robot
sets and specifies passive vs safe mode :
var = raw_input("*rp for reset and passive, d to disconnect, r to reset, s for safe, dr for drive*, e for exit")
var = raw_input("*rp for reset and passive, d to disconnect, r to reset, s for safe, dr for drive*, ! for stop, e for exit")
distinguishes choices : choices = raw_input("*enter 1 for reading raw input and enter 2 to read sensor*")


reading.py

reads and interprets sensor readings
driver
stops roomba

