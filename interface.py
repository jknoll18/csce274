import serial
import struct
import threading

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
      return True
    else:              ## clean not clean
      print('not active')
      return False

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
      if v >= 501 or r >= 2001: 
      self.close()
      else: ##statement or leave
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
  def time(seconds,velocity,radius):
    timerO = Timer(seconds, drive(velocity,radius))
    timer0.start()
  def penta():  ## read buttons then excute this
    drive(30,768)  ##timer needed? Assuming 768 is straight
    time(9.0,30,576)
    time(18.0,30,384) ## does timer do it all at once
    time(27.0,30,576)
    time(36.0,30,384)
    stop()  ## stops the roomba
