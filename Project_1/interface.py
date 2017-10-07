import serial
import struct
from threading import Timer

class Interface:
  def __init__(self):
    self.connect()
    self.passive() ##is this right
    self.safe()
  ##allows connection to the robot with a baudrate of 115200
  def connect(self):
    self.serial_connection = serial.Serial('/dev/ttyUSB0', 115200)
  ##function that allows the user to use the built_in write function to do an action
  def write_raw(self,raw_command):  
    self.serial_connection.write(raw_command)
  ##this will read the number of bytes use for each function and return a hex value
  def read_raw(self,num_bytes):
    raw_data = self.serial_connection.read(num_bytes)
    return raw_data

  ##function that will read the sensor depending on what sensor pack it is use
  def read_sensor(self, sensor_packet_id):
    """
    Args:
      sensor_packet_id (int): ID of the sensor packet.
    """
    # write
    sense = int(sensor_packet_id)
    raw_command = chr(142) + chr(sense)
    self.serial_connection.write(raw_command)
        
    # read raw
        
    var = self.serial_connection.read(1)
        
    # Processing
    val = struct.unpack('B',var)[0] ## find out why only prints out as 0 
    print val
    if val == 1:
      print('active')
      return True
    else:              ## clean not clean
      print('not active')
      return False
  ## the purpose for this function is to choose which of the multiple functions will be used 
  ##depending on what keyword it is shown in the prompt when the main file is compiled
  def command(self,var): ##function that calls functions depeding on input
    if var == "rp":
      raw_command = chr(128)
      self.write_raw(raw_command)    ##should we change the nums to 1,2,3 instead of the specific numbers
    elif var == "d": ##this statement will clsoe the program
      self.close()
    elif var == "r":##this statement will reset the robot
      self.reset()
    elif var == "rp":## this statement will set the robot to passive by calling the passive function
      self.passive()
    elif var == "cl": ## maybe put something in for all button presses
      self.clean()
    elif var == "s":
      self.safe()
    elif var == "!":
      self.stop()
    elif var == "dr":## this statement will allow the user to imput the velocity and radius at which the robot will move
      self.safe()
      print("enter velocity")
      velocity = raw_input()##allows the user to input a value for the velocity of the robot
      print("enter radius")
      radius = raw_input()## allows the user to input a value for the radius that the robot is moving
      self.drive(velocity,radius)##calls the drive function and uses the velocity and radius that user inputs
    elif var == "pe":##this will tell what keyword to press to start the pentagon drive function
      self.penta()##calls the pentagon drive fucntionfunction
    else:
      is_connected = False
      self.close()
  def stop(self):  ##the stop function to the robot
    self.serial_connection.write(chr(173))
  def close(self):
    self.serial_connection.close()
  def reset(self):  ##the reset function to reset the robot and put it into passive
    self.serial_connection.write(chr(7))
  def passive(self):  ##the passive function reconnects the robot to the original passive state
    self.serial_connection.write(chr(128))
  def clean(self):
    self.serial_connection.write(chr(165))[0]  ## is this how it works on page 17?
  def safe(self):  ##the safe function sets the robot to the state safe
    self.serial_connection.write(chr(131))
  ##this is the drive function that will allow the user to input a velocity value and radius of how 
  ##the robot should be moving
  def drive(self,velocity,radius): ## drive function
     ## put in error checking
     ##the hex values were needed to convert both variables into hex values
     ##allow us to use them in the unpack funcion of struct
     v = int(velocity) & 0xffff
     r = int(radius) & 0xffff
     ##this allows us to put the two variable into 2's complements
     pack =struct.unpack('4B',struct.pack('>2H',v,r))
     ## this is the command giving in the manual for drive
     opcode = (137,)
     data = opcode + pack
     ##byte packs data to be a chr value which will be used to input in the write function
     byte = struct.pack('B' * len(data), *data)
     self.serial_connection.write(byte) # execute drive
  def stream(self,num_packets,packet_id):## streams i tried to setup
    code_stream = chr(148) + chr(num_packets) + chr(packet_id)
    self.serial_connection.write(code_stream)
  def stopStream(self,state):  ##function to stop the stream
    code_stream2 = chr(150) + chr(state)

  ##def time(self,seconds,velocity,radius):
   ## timer0 = threading.Timer(seconds, self.drive(velocity,radius))
   ## timer0.start()
  ##this is the pentagon drive function, which allows the robot to move in a pentagon formation
  ##the drive function and the Timer function from the threading class was used to 
  ##allow us to set a timer at which each segment of the pentagon the robot should move
  def penta(self):  ## read buttons then excute this
    ##drive(30,768)  ##timer needed? Assuming 768 is straight
    ##the reason why we used args to intialize the velocity and radius was due to an error that we were 
    ##getting called nonetype. 
    timer0 = Timer(0.0,self.drive,args=(100,32768))
    timer0.start()
    timer1 = Timer(3.0,self.drive,args=(300,1))
    timer1.start()
    timer2 = Timer(3.4,self.drive,args=(100,32768))
    timer2.start()
    timer3 = Timer(5.9,self.drive,args=(300,1))
    timer3.start()
    timer4 = Timer(6.5,self.drive,args=(100,32768))
    timer4.start()
    timer5 = Timer(9.5,self.drive,args=(300,1))
    timer5.start()
    timer6 = Timer(10.1,self.drive,args=(100,32768))
    timer6.start()
    timer7 = Timer(12.6,self.drive,args=(300,1))
    timer7.start()
    timer8 = Timer(13.0,self.drive, args=(100,32768))
    timer8.start()
    timer9 = Timer(16.8,self.drive, args=(300,1))
    timer9.start()
    timerA = Timer(17.2,self.stop)
    timerA.start()

    
    ##self.time(1.0,30,384) ## does timer do it all at once
    ##self.time(3.0,30,576)
    ##self.time(5.0,30,384)
    ##self.stop()  ## stops the roomba
    