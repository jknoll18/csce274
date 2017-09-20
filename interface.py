import serial
import struct

class interface:

 def connect():
    serial_connection = serial.Serial('/dev/ttyUSB0', 115200)
    
    return serial_connection
 def read(serial conn):
   conn = serial.Serial('/dev/ttyUSB0', 115200) 
   string var = con.read(1)
   int val = struct.unpack('B',var)
   if val = 10:
     print('safe')
   else 
     print('passive')
 def command(int num, serial conn):
   if num = 128:
     def start():
       
   elif num = 173:    
     def stop():
   elif num = 7:
     def reset():
   elif num = 128:
     def passive():
   elif num = 131:
     def safe():
   elif num = 137:
     def drive():
