"""Hey I uploaded this as a separate file because I didn't want to mess up what you guys already have.
add this to def read_sensor
let me know if anything looks wrong I'm going to try and finish this in next couple of days
"""
    elif (sense == 45): ##Light Bumper
      lightbump = struct.unpack('B', var)[0]
      bits = "{0:6b}".format(lightbump)
      if(bits[0] =='1'):
        print 'Right Bumper Active'
        # TODO Check Packet ID 51 to see the signal strength (unsigned 16-bit value)
      if (bits[1] == '1'):
        print 'Right Front Bumper Active'
        # TODO Check Packet ID 50 to see the signal strength
      if (bits[2] == '1'):
        print 'Right Center Bumper Active'
        # TODO Check Packet ID 49 to see the signal strength
      if (bits[3] == '1'):
        print 'Left Center Bumper Active'
        # TODO Check Packet ID 48 to see the signal strength
      if (bits[4] == '1'):
        print 'Left Front Bumper Active'
        # TODO Check Packet ID 47 to see the signal strength
      if (bits[5] == '1'):
        print 'Left Bumper Active'
        # TODO Check Packet ID 46 to see the signal strength
      return bits
   
