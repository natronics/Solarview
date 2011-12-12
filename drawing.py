import solarsystem
import datetime

class DrawSVG(object):
  
  def __init__(self, w, h, zoom, center=0):
    self.width = w
    self.height = h
    self.zoom = zoom
    
    self.document = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   version="1.1"
   width="%(w)d"
   height="%(h)d"
   id="solarsystemsvg">
  <defs id="defs4" />
  <metadata id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="The Solar System in SVG">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title>The Solar System in SVG</dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
   <rect
     style="fill:#000000;fill-opacity:1;"
     width="%(w)d"
     height="%(h)d"
     x="0"
     y="0" />""" % {"w": self.width, "h": self.height}
  
  
  @staticmethod
  def map_range(out_low, out_high, range_low, range_high, val):
    a = float(out_high - out_low) / float(range_high - range_low)
    b = out_low - a * range_low
    """
    if val < range_low:
      return out_low
    if val > range_high:
      return out_high
    """
    return (a * val) + b
  
  def HAE2Screen(self, x,y):
    x_screen = DrawSVG.map_range(0          , self.width, -self.zoom, self.zoom, x)
    y_screen = DrawSVG.map_range(self.height, 0         , -self.zoom, self.zoom, y)
    return (x_screen, y_screen)

  def draw_orbit(self, orbit_HAE, color="#5f6e91", stroke=0.7, alpha=0.5, dashed=False):
    
    first_point = self.HAE2Screen(orbit_HAE[0][0],orbit_HAE[0][1])
    if dashed:
      svg = """<path style="fill:none;stroke:%s;stroke-width:%0.2fpx;stroke-opacity:%0.1f;stroke-dasharray:3,3;" d="M %0.4f,%0.4f L""" %  (color, stroke, alpha, first_point[0], first_point[1])
    else:
      svg = """<path style="fill:none;stroke:%s;stroke-width:%0.2fpx;stroke-opacity:%0.1f;" d="M %0.4f,%0.4f L""" %  (color, stroke, alpha, first_point[0], first_point[1])
    
    for o in orbit_HAE[1:]:
      point = self.HAE2Screen(o[0],o[1])
      svg += "%0.4f,%0.4f " % (point[0],point[1])
      
    svg += """" />"""
    self.document += svg
 
  def draw_object(self, pos, size, color, alpha, label=None):
    point = self.HAE2Screen(pos[0], pos[1])
    svg = """<circle cx="%0.4f" cy="%0.4f" r="%0.3f" style="fill:none;stroke-width:0;fill:%s;fill-opacity:%0.2f;" />""" % (point[0], point[1], size, color, alpha) 
    self.document += svg
  
  def draw_label(self, pos, text, color, size, screen=False):
    if screen:
      point = pos
    else:
      point = self.HAE2Screen(pos[0], pos[1])
    svg = """<text
     x="0"
     y="0"
     id="text%s"
     xml:space="preserve"
     style="font-size:%0.1fpx;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;text-align:start;line-height:125%%;letter-spacing:0px;word-spacing:0px;writing-mode:lr-tb;text-anchor:start;fill:%s;fill-opacity:1;stroke:none;font-family:Helvetica CE;-inkscape-font-specification:Helvetica CE"><tspan
       x="%f"
       y="%f">%s</tspan></text>""" % (text, size, color, point[0]+3, point[1]-3, text)
    self.document += svg
  
  def draw_solarsystem(self, dt, draw_orbits = True):
    
    if draw_orbits:
      for planet in solarsystem.planets:
        orbit = solarsystem.get_orbit(planet.eph, dt, dt + datetime.timedelta(days = planet.year))
        self.draw_orbit(orbit)
    
    for planet in solarsystem.planets:
      position = solarsystem.position(planet.eph, dt)
      size = planet.radius*2
      if size < 0.6: size = 0.6
      if size > 5: size = 5
      self.draw_object(position, size, planet.color, 1)
    
    self.draw_object((0,0,0), 5, "#eaff2e", 1)

  def draw_ephemobject(self, obj, dt, label=None):
    position = solarsystem.position(obj, dt)
    size = 0.56
    self.draw_object(position, size, "#ffffff", 1)
    
    if label != None:
      self.draw_label(position, label, "#dddddd", 7)
  
  
  def write(self, filename):
    handle = open(filename, 'w')
    
    self.document += "\n</svg>"
    
    handle.write(self.document)
    handle.close()
    
