import serial
import struct

class Interface:
  def __init__(self):
    self.connect()

  def connect(self):
    self.serial_connection = serial.Serial('/dev/ttyUSB0', 115200)

  def write_raw(raw_command):
    self.serial_connection.write(raw_command);

  def read_raw(num_bytes):
    raw_data = self.serial_connection.read(num_bytes);
    return raw_data


  def read_sensor(self, sensor_packet_id):
    """
    Args:
      sensor_packet_id (int): ID of the sensor packet.
    """
    # write
    raw_command = chr(142) + chr(sensor_packet_id)
    self.serial_connection.write(raw_command)
        
    # read raw
        
    var = self.serial_connection.read(1)
        
    # Processing
    val = struct.unpack('B',var)[0]
    if val == 10:
      print('safe')
    else:
      print('passive')

  def command(self, num):
    if num == 128:
      raw_command = chr(128)
      self.write_raw(raw_command)    ##should we change the nums to 1,2,3 instead of the specific numbers
    elif num == 173:
      self.stop()
    elif num == 7:
      self.reset()
    elif num == 128:
      self.passive()
    elif num == 131:
      self.safe()
    elif num == 137:
	  ##look if there is a condition for drive
      self.drive()
	  
	  
  def stop():  ##the stop function to exit out ot the interface
    self.write(chr(173))
  def reset():  ##the reset function to reset the robot and put it into passive
    self.write(chr(7))
  def passive():  ##the passive function reconnects the robot to the original passive state
    self.write(chr(128))
  def safe():  ##the safe function sets the robot to the state safe
    self.write(chr(131))
  def drive():
    ## write with velocity and radius
