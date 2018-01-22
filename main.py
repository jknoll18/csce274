from interface import Interface
from reading import Reading
def Main(args=None):
  ##creates a main for the interface
  print("*Welcome to the robot interface*")
  ##demo
  str = raw_input("*Press c to connect to the robot*")
  if str == "c":
    inter = Interface()
    read = Reading()
    cond = raw_input("*enter a for commands, enter b for reading, enter c for exit*")
    if cond == "a":
      is_go = False
      while is_go == False:
        print("*enter the number you want for the command*")
        var = raw_input("*rp for reset and passive, ra2 for reading button, d to disconnect, r to reset\n sa for safe,pdc for pd controller, dr for drive*,pe for Pentagon drive, ! for stop, e for exit\n , f for full mode, drd for drive direct,p for play,so for song:")
        if var == "e":
          is_go = True
          inter.close()
        if var == "ra":
          read.isActive()
        if var == "ra2":
          inter.full()
          read.isActive2()
        if var == "wall":
          read.wall()
        if var == "pdc":
          read.pdcontroller()
        if var == "para":
          read.pararun()
        if var == "IC3":
          read.testIC3()
        if var == "IC5":
          read.testIC5()
        if var == "p":
          inter.play(0)
          ##inter.play(1)
        if var == "so":
          inter.song()
        else:
          inter.command(var)
    if cond == "b":
      inter.passive()
      choices = raw_input("*enter 1 for reading raw input and enter 2 to read sensor*")
      if choices == "1":
        raw_bytes = raw_input("*enter the number of bytes to read*")
        inter.read_raw(raw_bytes)
      if choices == "2":
        sensor_id = raw_input("*enter the sensor packet id*")
        inter.read_sensor(sensor_id)
    if cond == "c":
      is_connected = False
      inter.close()
  else:
    is_connected = False
    inter.close()
Main()
