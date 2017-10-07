import serial
import struct
from threading import Timer

class Interface:
  def __init__(self):
    self.connect()
    self.passive() ##is this right
    self.safe()

  def connect(self):
    self.serial_connection = serial.Serial('/dev/ttyUSB0', 115200)

  def write_raw(self,raw_command):  
    self.serial_connection.write(raw_command)

  def read_raw(self,num_bytes):
    raw_data = self.serial_connection.read(num_bytes)
    return raw_data


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
      return val
    else:              ## clean not clean
      print('not active')
      return val

  def command(self,var): ##function that calls functions depeding on input
    if var == "rp":
      raw_command = chr(128)
      self.write_raw(raw_command)    ##should we change the nums to 1,2,3 instead of the specific numbers
    elif var == "d":
      self.close()
    elif var == "r":
      self.reset()
    elif var == "rp":
      self.passive()
    elif var == "cl": ## maybe put something in for all button presses
      self.clean()
    elif var == "s":
      self.safe()
    elif var == "!":
      self.stop()
    elif var == "dr":
      self.safe()
      print("enter velocity")
      velocity = raw_input()
      print("enter radius")
      radius = raw_input()
      self.drive(velocity,radius)
    elif var == "pe":
      self.penta()
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
  def drive(self,velocity,radius): ## drive function
     v = int(velocity) & 0xffff
     r = int(radius) & 0xffff
     if v <= -501 or v >= 501: 
       exit(0)
     ##elif r <= -2001 or r >= 2001:
       ##exit(0)
     else:
       pack =struct.unpack('4B',struct.pack('>2H',v,r))
       opcode = (137,)
       data = opcode + pack
       byte = struct.pack('B' * len(data), *data)
       self.serial_connection.write(byte) # execute drive
  def stream(self,num_packets,packet_id):## streams i tried to setup
    code_stream = chr(148) + chr(num_packets) + chr(packet_id)
    self.serial_connection.write(code_stream)
  def stopStream(self,state):  ##function to stop the stream
    code_stream2 = chr(150) + chr(state)
  ##def time(self,seconds,velocity,radius):
    ##timerO = threading.Timer(seconds, self.drive(velocity,radius))
    ##timer0.start()
  def penta(self):  ## read buttons then excute this
    timer0 = Timer(0.0,self.drive,args=(100,32768))
    timer0.start()                              ## 3 interval str
    timer1 = Timer(3.0,self.drive,args=(300,1))
    timer1.start()                              ## 0.4 interval turn
    timer2 = Timer(3.4,self.drive,args=(100,32768))
    timer2.start()                               ## 2.5 interval
    timer3 = Timer(5.9,self.drive,args=(300,1))
    timer3.start()                               ## 0.6 interval
    timer4 = Timer(6.5,self.drive,args=(100,32768))
    timer4.start()                                ## 3 interval
    timer5 = Timer(9.5,self.drive,args=(300,1))
    timer5.start()                                 ## 0.6 interval
    timer6 = Timer(10.1,self.drive,args=(100,32768))
    timer6.start()                                 ## 2.5 interval
    timer7 = Timer(12.6,self.drive,args=(300,1))
    timer7.start()                                 ## 0.4 interval
    timer8 = Timer(13.0,self.drive, args=(100,32768))
    timer8.start()                                  ## 3.8 interval
    timer9 = Timer(16.8,self.drive, args=(300,1))
    timer9.start()                                  ## 0.4 interval
    timerA = Timer(17.2,self.stop)
    timerA.start()

