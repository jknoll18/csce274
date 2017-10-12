import serial
import struct
from threading import Timer
class Interface:
  def __init__(self):
    self.connect()
    self.passive() 
    self.safe()

  def connect(self):
    self.serial_connection = serial.Serial('/dev/ttyUSB0', 115200)
    self.passive() 
    self.safe()

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
    if (sense == 18 or sense == 8 or sense == 9 or sense == 10 or sense == 11 or sense == 12 or sense == 13):
      val = struct.unpack('B',var)[0]
      if val == 1:
        print('active')
        return 1
      else:              ## clean not clean
        print('not active')
        return 0
    elif (sense == 7):
      bumpR = struct.unpack('B',var)[0]
      bumpL = struct.unpack('B',var)[1]
      WDR = struct.unpack('B',var)[2]
      WDL = struct.unpack('B',var)[3]
    ##look up how to convert a string hex into a signed int.
    ##it both distance and angle we need to find the raw encoder count 
    ##using this formula, it's sensor packet 43, 44
    ## N counts * (mm in 1 wheel revolution / counts in 1 wheel revolution) = mm
    ##N counts * (π * 72.0 / 508.8) = mm
    elif (sense == 19):
      pack =struct.unpack('4B',struct.pack('>2H', var))
    elif (sense == 20):
      pack =struct.unpack('4B',struct.pack('>2H', var))
    else:
      exit(0)

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
    elif var == "j":
	  self.test()
    elif var == "f":##this will set the robot to full mode
      self.full()
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
     ## put in error checking
     v = int(velocity) & 0xffff
     r = int(radius) & 0xffff
     pack =struct.unpack('4B',struct.pack('>2H',v,r))
     opcode = (137,)
     data = opcode + pack
     byte = struct.pack('B' * len(data), *data)
     self.serial_connection.write(byte) # execute drive
  def full(self):
    self.serial_connection.write(chr(132))
  def stream(self,num_packets,packet_id):## streams i tried to setup
    code_stream = chr(148) + chr(num_packets) + chr(packet_id)
    self.serial_connection.write(code_stream)
  def stopStream(self,state):  ##function to stop the stream
    code_stream2 = chr(150) + chr(state)

  ##def time(self,seconds,velocity,radius):
   ## timer0 = threading.Timer(seconds, self.drive(velocity,radius))
   ## timer0.start()

  def penta(self):  ## read buttons then excute this
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
    timer6 = Timer(9.9,self.drive,args=(100,32768))
    timer6.start()
    timer7 = Timer(12.4,self.drive,args=(300,1))
    timer7.start()
    timer8 = Timer(13.0,self.drive, args=(100,32768))
    timer8.start()
    timer9 = Timer(15.8,self.drive, args=(300,1)) 
    timer9.start()
    timerA = Timer(16.2,self.stop)
    timerA.start()
    
