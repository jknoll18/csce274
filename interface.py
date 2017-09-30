import serial
import struct
import threading

class Interface:
  def __init__(self):
    self.connect()
	## passive() for task 3a?
	## safe()

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
    self.serial_connection.write_raw(raw_command)
        
    # read raw
        
    var = self.serial_connection.read(1)
        
    # Processing
    val = struct.unpack('B',var)[0] ## change this please
    if val == 10:
      print('safe')
    else:
      print('passive')

  def command(self, num):
    if num == 128:
      raw_command = chr(128)
      self.write_raw(raw_command)    ##should we change the nums to 1,2,3 instead of the specific numbers
    elif num == 173:
      stop()
    elif num == 7:
      reset()
    elif num == 128:
      passive()
	elif num == 165: ## maybe put something in for all button presses
	  clean()
    elif num == 131:
      safe()
    elif num == 137:
	  print('enter velocity')
	  if(-500 <= input() <= 500):
	    velocity = input()
	  else:
	    print('not a vaild value, please enter a value between -500 and 500')
   		exit(0) ## put a loop in?
	  print('enter radius')
	  if(-2000 <= input() <= 2000):
	  radius = input()
      drive(velocity,radius)
	  else:
	    print('not a vaild value, please enter a value between -2000 and 2000')
	    exit(0)
  def toHex(value, bit-length):
    return hex((value + (1 << bit-length)) % (1 << bit-length))
  def bytes(number):
    return divmod(number,0x100)  
  def stop():  ##the stop function to exit out ot the interface
    self.write(chr(173))
  def reset():  ##the reset function to reset the robot and put it into passive
    self.write(chr(7))
  def passive():  ##the passive function reconnects the robot to the original passive state
    self.write(chr(128))
  def clean():
    self.write(chr(165))[0]  ## is this how it works on page 17?
  def safe():  ##the safe function sets the robot to the state safe
    self.write(chr(131))
  def drive(velocity,radius):
    hex_v = toHex(velocity,16)
	hev_r = toHex(radius,16)
	high_v, low_v = bytes(hex_v)
	high_r, low_r = bytes(hev_r)
	high_vd = int(high_v,16)
	low_vd = int(low_v,16)
    high_rd = int(high_r,16)
	low_rd = int(low_r,16)
	self.write(chr(137))[high_vd][low_vd][high_rd][low_rd]
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