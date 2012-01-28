import telnetlib
import datetime

class Horizons(object):

  HOST = "horizons.jpl.nasa.gov"
  PORT = 6775
  ESC = chr(0x1b)
  
  def __init__(self):
    self.now = datetime.datetime.utcnow()
    self.now_str = self.now.strftime('%Y-%b-%d %H:%M')
    next = self.now + datetime.timedelta(0,3600)
    self.next_str = next.strftime('%Y-%b-%d %H:%M')
    


  def dump_telnet_out(self, code, start, end):
    
    start_str = start.strftime('%Y-%b-%d %H:%M')
    end_str   =   end.strftime('%Y-%b-%d %H:%M')
    
    self.OE_tree = [('<cr>:',               'E\n')                  # Ephemeris
              , ('[o,e,v,?] :',             'v\n')                  # Vectors
              , ('[ <id>,coord,geo  ] :',   '500@10\n')             # Sol body center
              , ('[ y/n ] -->',             'y\n')                  # Confirm
              , ('[eclip, frame, body ] :', 'eclip\n')              # Frame Coords
              , ('] :',                     "%s\n" % start_str)     # Begin Time
              , ('] :',                     "%s\n" % end_str)       # End Time
              , ('? ] :',                   '6h\n')                 # Interval
              , ('?] :',                    'n\n')                  # Defaults?
              , ('[J2000, B1950] :',        'J2000\n')              # J2000 Coords
              , ('LT+S ]  :',               '1\n')                  # No lt correction
              , ('3=KM-D] :',               '2\n')                  # AU/D
              , ('YES, NO ] :',             'YES\n')                # CSV
              , ('YES, NO ] :',             'NO\n')                 # No labels
              , ('[ 1-6, ?  ] :',           '1\n')]                 # Ouput table type?
  
    telnet = telnetlib.Telnet(self.HOST, self.PORT)
    #telnet.set_debuglevel(1)
    
    print 'Waiting for Horizons...'
    
    telnet.read_until('Horizons>')
    telnet.write("%s\n" % code)

    for cue in self.OE_tree:
      telnet.read_until(cue[0])
      telnet.write(cue[1])

    elements = telnet.read_until('$$EOE')
    elements = elements.split('$$SOE')[1]
    elements = elements.strip('$$EOE')
    
    telnet.close()
    
    return elements
    
  def get_track(self, code, start, end):
    
    data = self.dump_telnet_out(code, start, end)
    
    data = data.split('\n')
    
    orbit = []
    
    for line in data[1:-1]:
      li = line.split(',')
      date = float(li[0])
      x    = float(li[2])
      y    = float(li[3])
      z    = float(li[4])
      
      date = int((date - 2440587.5) * 86400)
      
      orbit.append({"dt": date, "point": (x,y,z)})
      #print date, x, y
      
    return orbit
