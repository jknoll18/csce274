import serial
import struct

class Interface:
  def __init__(self):
    self.connect()

  def connect(self):
    self.serial_connection = serial.Serial('/dev/ttyUSB0', 115200)

  def write_raw(raw_command):
    self.serial_connection.write(raw_command)

  def read_raw(num_bytes):
    raw_data = self.serial_connection.read(num_bytes)
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
      self.write_raw(raw_command)    
    elif num == 173:
      self.stop()
    elif num == 7:
      self.reset()
    elif num == 128:
      self.passive()
    elif num == 131:
      self.safe()
    elif num == 137:
      self.drive()
