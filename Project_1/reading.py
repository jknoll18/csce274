from interface import Interface
from threading import Timer
class Reading: 
  def __init__(self):
    press = False
  def isActive(self):
    count = 0
    state = 1
    while count < 5:
      sw = Interface().read_sensor(18)
      if sw == 1:
        state += 1
        if state % 2 == 0:
          Interface().penta()
          count += 1
        else:
          Interface().stop
      if sw == 0:
        if state % 2 == 0:
          Interface().penta()
          count += 1
        else:
          Interface().stop  