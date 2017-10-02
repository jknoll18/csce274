from interface import Interface

def main(args=None):
  ##creates a main for the interface
  print("*Welcome to the robot interface*")
  str = raw_input("*Press c to connect to the robot*")
  if str == "c":
    inter = Interface()
    cond = raw_input("*enter a for commands, enter b for reading, enter c for exit*")
    if cond == "a":
      print("*enter the number you want for the command*")
      var = raw_input("*rp for reset and passive, d to disconnect, r to reset, s for safe, dr for drive*")
      inter.command(var)
    if cond == "b":
      choices = raw_input("*enter 1 for reading raw input and enter 2 to read sensor*")
      if choices == "1":
        raw_bytes = raw_input("*enter the number of bytes to read*")
        inter.read_raw(raw_bytes)
      if choices == "2":
        sensor_id = raw_input("*enter the sensor packet id*")
        inter.read_sensor(sensor_id)
    if cond == "c":
      exit(0)
  else:
    exit(0)
main()