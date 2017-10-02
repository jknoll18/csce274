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
    raw_command = chr(142) + chr(sensor_packet_id)
    self.serial_connection.write_raw(raw_command)
        
    # read raw
        
    var = self.serial_connection.read(1)
        
    # Processing
    val = struct.unpack('B',var)[0] ## change this please
    if val == 10:
      print('safe')
    else:
      print('passive')

  def command(self,var): ##function that calls functions depeding on input
    if var == "rp":
      raw_command = chr(128)
      self.write_raw(raw_command)    ##should we change the nums to 1,2,3 instead of the specific numbers
    elif var == "d":
      self.stop()
    elif var == "r":
      self.reset()
    elif var == "rp":
      self.passive()
    elif var == "cl": ## maybe put something in for all button presses
      self.clean()
    elif var == "s":
      self.safe()
    elif var == "dr":
      print('enter velocity')
      velocity = input()
      print('enter radius')
      radius = input()
      self.drive(velocity,radius)
    else:
      exit(0)
  def toHex(value, bit_length):
    return hex((value + (1 << bit_length)) % (1 << bit_length))
  def bytes(number):
    return divmod(number,0x100)  
  def stop(self):  ##the stop function to exit out ot the interface
    self.serial_connection.write(chr(173))
  def reset(self):  ##the reset function to reset the robot and put it into passive
    self.serial_connection.write(chr(7))
  def passive(self):  ##the passive function reconnects the robot to the original passive state
    self.serial_connection.write(chr(128))
  def clean(self):
    self.serial_connection.write(chr(165))[0]  ## is this how it works on page 17?
  def safe(self):  ##the safe function sets the robot to the state safe
    self.serial_connection.write(chr(131))
  def drive(self,velocity,radius): ## drive function
    hex_v = toHex(velocity,16)  ## converts the velocity and radius to hexadecimal
    hev_r = toHex(radius,16)
    high_v, low_v = bytes(hex_v) ##splits the hexadecimal to high and low
    high_r, low_r = bytes(hev_r)
    high_vd = int(high_v,16)  # converts the each high and low to decimal
    low_vd = int(low_v,16)
    high_rd = int(high_r,16)
    low_rd = int(low_r,16)
    self.serial_connection.write(chr(137))[high_vd][low_vd][high_rd][low_rd] # execute drive
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