import ephem
import datetime
import config
import json
from math import fabs
from math import pi
from math import sin
from math import cos

class planet(object):
  
  def __init__(self, eph, a, year, radius, color, color_rgb):
    self.eph        = eph
    self.a          = a
    self.year       = year
    self.radius     = radius
    self.color      = color
    self.color_rgb  = color_rgb
    
planets = [   planet(ephem.Mercury() , 0.466,   87.969,  0.3829, "#c8c8c8", (0.784,0.784,0.784))
            , planet(ephem.Venus()   , 0.728,  224.700,  0.949 , "#f2dcb4", (0.949,0.863,0.706))
            , planet(ephem.Sun()     , 1    ,  365.245,  1     , "#55a8de", (0.333,0.659,0.871))
            , planet(ephem.Mars()    , 1.665,  686.971,  0.533 , "#d4624a", (0.831,0.384,0.290))
            , planet(ephem.Jupiter() , 5.458, 4332.59 , 11.21  , "#f2dcb4", (0.949,0.863,0.706))
          ]

class spacecraft(object):
  
  crafts = ["msl"]
  origin = datetime.datetime(1970,1,1,0,0,0)
  
  def __init__(self):
    self.data   = json.loads(open(config.datafile, 'r').read())
    
  def get_location(self, craft, dt):
    
    now = (dt - self.origin)
    now = int((now.days*86400) + now.seconds)
    
    spacecraft = self.data[craft]
    
    start = self.origin + datetime.timedelta(seconds=spacecraft["start"])
    
    i = 0
    m = 1e15
    m_i = 0
    for o in spacecraft["orbit"]:
      time = o["dt"]
      d = fabs(time - now)
      if d < m: 
        m   = d
        m_i = i
      
      #print o["dt"], i
      i+=1
    
    print m_i, spacecraft["orbit"][m_i]
    
    return 1.1, 0.2
  
def sphere2xyz(r, p, t):
  t = t-pi
  x = r * sin(p) * cos(t)
  y = r * sin(p) * sin(t)
  z = r * cos(p)
  
  return (x,y,z)

def position(obj, dt):
  obj.compute(dt)
 
  if obj.name == ephem.Sun().name:
    (x,y,z) = sphere2xyz(obj.earth_distance, obj.hlat - pi/2.0, obj.hlon)
  else:
    (x,y,z) = sphere2xyz(obj.sun_distance, obj.hlat - pi/2.0, obj.hlon)
    
  return (x,y)

def get_orbit(obj, begin, end, steps=180):
  dt = float((end - begin).days + ((end - begin).seconds / 86400))
  dt = dt / float(steps)
  orbit = []
  for i in range(steps):
    time = begin + datetime.timedelta(days=(i*dt))
    orbit.append(position(obj, time))
  orbit.append(position(obj, end))
  return orbit

def make_ephem_object(elements):
  
    e = {}
    if elements['Elements']['Eccentricity'] < 1:
      e = ephem.EllipticalBody()
    
    e.name        = elements['name']
    e._inc        = elements['Elements']['Inclination']
    e._Om         = elements['Elements']['LAAN']
    e._om         = elements['Elements']['Argument_of_Periapsis']
    e._a          = elements['Elements']['Semimajor_Axis']
    e._e          = elements['Elements']['Eccentricity']
    e._M          = elements['Elements']['Mean_Anomaly']
    epoch_date    = elements['Elements']['Epoch'] - 2415020 # JD to DJD
    
    e._epoch_M    = ephem.Date(epoch_date)
    e._epoch      = ephem.Date('2000/1/1')
    
    return e
