import serial
import struct
import time
import math
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
    if sense == 46 or sense==48 or sense==47 or sense== 50 or sense == 51 or sense==49:
      var2 = self.serial_connection.read(2)   
    else:
      var = self.serial_connection.read(1)
      ##since Distance and angle are 2 bits we should create another variable
    ## Processing
    if (sense == 18 or sense == 8 or sense == 9 or sense == 10 or sense == 11 or sense == 12 or sense == 13):
      val = struct.unpack('>B',var)[0]
      if val == 1:
        ##print('active')
        return 1
      else:              ## clean not clean
        ##print('not active')
        return 0
    elif (sense == 7):
      bumpdrop = struct.unpack('B',var)[0]
      bins = "{0:4b}".format(bumpdrop) 
      if(bins[0] =="1"):
        print 'LWD Active'
      if (bins[1] == "1"):
        print 'RWD Active'
      if (bins[2] == "1"):
        print 'LB Active'
      if (bins[3] == "1"):
        print 'RB Active'	    
      return bins
    elif (sense == 45):
      LBsensor = struct.unpack('>B',var)[0]
      bins = "{0:6b}".format(LBsensor)
      if(bins[0] =="1"):
        print 'bump right  Active'
      if (bins[1] == "1"):
        print 'BFR Active'
      if (bins[2] == "1"):
        print 'BCR Active'
      if (bins[3] == "1"):
        print 'BCL Active'
      if (bins[4] == "1"):
        print 'BFL active'
      if( bins[5] == "1"):
        print 'BL active'
      return bins
    elif (sense == 46):
      val = struct.unpack('>H',var2)[0]
      linval = math.sqrt(val)
      print linval
      return linval
    elif (sense == 47):
      val = struct.unpack('>H',var2)[0]
      linval = math.sqrt(val)
      print linval
      return linval
    elif (sense == 48):
      val = struct.unpack('>H',var2)[0]
      linval = math.sqrt(val)
      print linval
      return linval
    elif (sense == 49):
      val = struct.unpack('>H',var2)[0]
      linval = math.sqrt(val)
      print linval
      return linval
    elif (sense == 50):
      val = struct.unpack('>H',var2)[0]
      linval = math.sqrt(val)
      print linval
      return linval
    elif (sense == 51):
      val = struct.unpack('>H',var2)[0]
      linval = math.sqrt(val)
      print linval
      return linval
    elif (sense == 52):
      val = struct.unpack('>B',var)[0]
      print "char left",val
      return val
    elif (sense == 53):
      val = struct.unpack('>B',var)[0]
      print "char right",val
      return val
    elif (sense == 17):
      val = struct.unpack('>B',var)[0]
      print "char omni",val
      return val
    elif (sense == 34):
      charge = struct.unpack('>B', var)[0]
      bins = "{0:1b}".format(charge)
      return bins
    ##look up how to convert a string hex into a signed int.
    ##it both distance and angle we need to find the raw encoder count 
    ##using this formula, it's sensor packet 43, 44
    elif (sense == 19):
      Dpack =struct.unpack('2B',struct.pack('>h', var))
    elif (sense == 20):
      Apack =struct.unpack('2B',struct.pack('>h', var))
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
    elif var == "sa":
      self.safe()
    elif var == "!":
      self.stop()
    elif var == "dr":
      print("enter velocity")
      velocity = raw_input()
      print("enter radius")
      radius = raw_input()
      f =self.serial_connection.write(chr(142)+chr(19))
      first = self.serial_connection.read(f)
      ##this creates a parallel thread that is running as the
      ##main code is runnin
      self.drive(velocity,radius)
      time.sleep(3)
      l = self.serial_connection.write(chr(142)+chr(19))
      last = self.serial_connection.read(l)
      lastd = struct.unpack('>h', last)[0]
      print "distance travel"
      print lastd
    elif var == "pe":
      self.penta()
    elif var == "j":
	  self.test()
    elif var == "f":##this will set the robot to full mode
      self.full()
    elif var == "drd":
      print("enter right wheel velocity")
      vR = raw_input()
      print("enter left wheel velocity")
      vL = raw_input()
      self.driveDirect(vR,vL)
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
     ##self.full()
     v = int(velocity) & 0xffff
     r = int(radius) & 0xffff
     pack =struct.unpack('4B',struct.pack('>2H',v,r))
     opcode = (137,)
     data = opcode + pack
     byte = struct.pack('B' * len(data), *data)
     self.serial_connection.write(byte) # execute drive
  ##this was an attempt on reading the distance and angle
  """
  def angDist(self,time):
    print("enter velocity")
    velocity = raw_input()
    print ("enter radius") 
    radius = raw_input()
    ##timer0 = Timer(0.0, )
    while(velocity<501 or velocity >-501 or radius<32769 or radius>-32769 ):
      if (radius == 32768 or radius == 32767):
        self.serial_connection.write(chr(142)+chr(19)) 
        first = self.iserial_connection.read(2)      
        firstd = struct.unpack('>h', first)
        ##this creates a parallel thread that is running 
        ##as the main code is running
        self.drive(velocity,radius)
        time.sleep(3)
        ##timer0.cancel()
        self.serial_connection.write(chr(142)+chr(19))
        last = self.serial_connection.read(2)
        lastd = struct.unpack('h', last)
        print (lastd ,firstd)
      else:
        self.serial_connection.write(chr(142)+chr(20))
        firstA = self.serial_connection.read(2)
        firstAr = struct.unpack('>h', firstA)
        ##this creates a parallel thread that is running 
        ##as the main code is running
        timer3 = Timer(0.0,self.drive,args=(velocity,radius))
        timer3.start()
        time.sleep(3)
        timer3.cancel()
        self.serial_connection.write(chr(142)+chr(20))
        lastA = self.serial_connection.read(2)
        lastAr = struct.unpack('>h', lastA)
        print (lastAr ,firstAr)
  """
  def driveDirect(self,velocityR,velocityL): ## put in error checking
    v1 = int(velocityR) & 0xffff
    v2 = int(velocityL) & 0xffff
    pack =struct.unpack('4B',struct.pack('>2H',v1,v2))
    opcode = (145,)
    data = opcode + pack
    byte = struct.pack('B' * len(data), *data)
    self.serial_connection.write(byte)
  def song(self):
    
    self.serial_connection.write(chr(140)+chr(0)+chr(9)+chr(55)+chr(64)+chr(48)+chr(64)+chr(51)+chr(16)+chr(53)+chr(16)+chr(55)+chr(64)+chr(48)+chr(64)+chr(51)+chr(16)+chr(53)+chr(16)+chr(50)+chr(64))

    self.serial_connection.write(chr(140)+chr(1)+chr(4)+chr(45)+chr(30)+chr(46)+chr(30)+chr(47)+chr(30)+chr(48)+chr(64))
  def play(self,songnum):
    self.serial_connection.write(chr(141)+ chr(songnum))
    ##print("Product of sum song won't work")
  def full(self):
    self.serial_connection.write(chr(132))
    time.sleep(0.125)
  def stream(self,num_packets,packet_id):## streams i tried to setup
    code_stream = chr(148) + chr(num_packets) + chr(packet_id)
    self.serial_connection.write(code_stream)
  def stopStream(self,state):  ##function to stop the stream
    code_stream2 = chr(150) + chr(state)

  def penta(self):  ## read buttons then excute this
    timer0 = Timer(0.0,self.drive,args=(100,1))
    timer0.start()
    timer1 = Timer(3.0,self.drive,args=(100,32768))
    timer1.start()
    """
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
    """
