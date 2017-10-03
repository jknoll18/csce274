from interface import Interface
def isActive()
  sw = Interface().read_sensor(18)
  if(sw == True):
    active()
  else:
    InActive()
def active():
  Interface().penta()
def InActive():
     ##need something to read the button press and execute penta, use threading?
	## create a stream of reading sensor 18 and then create a active function for when active and in_active function
	## in active, if in the active run penta, if in_active while in active close off penta(lock)
	## in in_active, if pressed go into active, if not pressed do nothing