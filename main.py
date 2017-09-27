import interface

def main(args=None):
  ##creates a main for the interface
	commands = interface();
  print("*Welcome to the robot interface*");
  print("*Press c to connect to the robot*");
  str = input();
    if str = c || str = C:
      commands.connect();
	  print("*enter 1 for commands, enter 2 for reading, enter 3 for exit*");
	  cond = input();
	  if cond = 1:
	    print("*enter the number you want for the command*");
	    var = input();
	    command(self,var);
      else:
	    exit(0);
	  if cond = 2:
        print("*enter 1 for reading raw input and enter 2 to read sensor*");
        choices = input();
		  if choices = 1:
		    print("*enter the number of bytes to read*");
			raw_bytes = input();
			read_raw(raw_bytes);
		  if choices = 2:
		    print("*enter the sensor packet id*");
			sensor_id = input();
			read_sensor(self,sensor_id);
      if cond = 3:
	    exit(0);