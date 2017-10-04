from interface import Interface
class reading:  
  def __init__(self):
    press = False
    touch =0
  def isActive():
    while():
      sw = Interface().read_sensor(18)
      if sw == '1':
        press = True 
      else:
        press = False
      self.doSomething()
  def doSomething(self):
    if press == True:
      if touch == 1:
        interface().penta()
      elif touch == 0:
        interface().stop()	  
     ##need something to read the button press and execute penta, use threading?
	## create a stream of reading sensor 18 and then create a active function for when active and in_active function
	## in active, if in the active run penta, if in_active while in active close off penta(lock)
	## in in_active, if pressed go into active, if not pressed do nothing