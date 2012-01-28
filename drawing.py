import solarsystem
import datetime
import cairo
from PIL import Image
from math import pi

class Map(object):
  def __init__(self, width, height, zoom, center):
    aspect = width/float(height)
    if width >= height:
      x_range = 2*zoom
      y_range = x_range / aspect
    else:
      y_range = 2*zoom
      x_range = y_range * aspect

    self.xa = -width / float(x_range)
    self.xb = 0 - self.xa * (x_range/2.0 + center[0])

    self.ya = -height / float(y_range)
    self.yb = 0 - self.ya * (y_range/2.0 + center[1])

  def map_x(self, value):
    return (self.xa * value) + self.xb

  def map_y(self, value):
    return (self.ya * value) + self.yb

class DrawPNG(object):
  """ A PNG Solar System Drawing class
        draw_line()
        draw_object()
        draw_text()
        draw_solarsystem()
        draw_ephemobject()
  """
  
  def __init__(self, w, h, zoom, center=(0,0)):
    self.width    = w
    self.height   = h
    
    self.map = Map(self.width, self.height, zoom, center)
    
    # construct an image surface and a drawing context
    self.surface  = cairo.ImageSurface(cairo.FORMAT_RGB24, self.width, self.height)
    self.cr       = cairo.Context(self.surface)
    
    # Space is black
    self.cr.set_source_rgb(0, 0, 0)
    self.cr.rectangle(0, 0, self.width, self.height)
    self.cr.fill()

  def HAE2Screen(self, x,y):
    """ Converts Cartesian Heliocentric Aeries Ecliptic coordinates in A.U. to 
        screen coordiates x,y with the maping helper class
    """ 
    x_screen = self.map.map_x(x)
    y_screen = self.map.map_y(y)
    return (x_screen, y_screen)
    
  def draw_object(self, pos, size, c, alpha):
    (x,y) = self.HAE2Screen(pos[0], pos[1])
    self.cr.set_source_rgba(c[0], c[1], c[2], alpha)
    self.cr.arc(x, y, size, 0, 2 * pi)
    self.cr.fill()
    
  def draw_line(self, line, line_width, c, alpha=0.8):
    self.cr.set_source_rgba(c[0], c[1], c[2], alpha)
    
    # First Point
    (x,y) = self.HAE2Screen(line[0][0], line[0][1])
    self.cr.move_to(x,y)
    
    for pos in line[1:]:
      (x,y) = self.HAE2Screen(pos[0], pos[1])
      self.cr.line_to(x,y)
      
    self.cr.set_line_width(line_width);
    self.cr.stroke()
  
  def draw_solarsystem(self, dt, draw_orbits=True, orbit_stroke=0.7, planet_scaler=2, planet_min=5, planet_max=15):
    """ Draws the solar system for a given time"""
    
    if draw_orbits:
      for planet in solarsystem.planets:
        orbit = solarsystem.get_orbit(planet.eph, dt, dt + datetime.timedelta(days = planet.year))
        self.draw_line(orbit, orbit_stroke, (0.373,0.435,0.569), 0.5)
    
    # Draw the Planets
    for planet in solarsystem.planets:
      position = solarsystem.position(planet.eph, dt)
      size = planet.radius*planet_scaler
      if size < planet_min: size = planet_min
      if size > planet_max: size = planet_max
      self.draw_object(position, size, planet.color_rgb, 1)
    
    # The Sun
    self.draw_object((0,0,0), planet_max+2, (0.918, 1, 0.180), 1)
  
  def draw_ephemobject(self, obj, dt, size=0.7, label_size=7, label=None, label_offset=10):
    position = solarsystem.position(obj, dt)
    self.draw_object(position, size, (1,1,1), 1)
  
    if label != None:
        self.draw_text(position, label, (0.8,0.8,0.8), label_size, label_offset=label_offset)
        
  def draw_text(self, pos, text, c, size, screen=False, label_offset=10):
    
    self.cr.set_source_rgb(c[0], c[1], c[2])
    self.cr.select_font_face("Helvetica CE", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    self.cr.set_font_size(size)
    
    if screen:
      x = pos[0]
      y = pos[1]
    else:
      (x,y) = self.HAE2Screen(pos[0], pos[1])
    
    #x_bearing, y_bearing, width, height = self.cr.text_extents("a")[:4]
    self.cr.move_to(x + label_offset, y - label_offset)
    self.cr.show_text(text)

  def write(self, filename):
    self.surface.write_to_png(filename)



















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
    #print point[0], point[1], size, color, alpha
    svg = """<circle cx="%0.4f" cy="%0.4f" r="%0.3f" style="fill:none;stroke-width:0;fill:%s;fill-opacity:%0.2f;" />""" % (point[0], point[1], size, color, alpha) 
    self.document += svg
  
  def draw_label(self, pos, text, color, size, screen=False, label_offset=10):
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
       y="%f">%s</tspan></text>""" % (text, size, color, point[0]+label_offset, point[1]-label_offset, text)
    self.document += svg
  
  def draw_solarsystem(self, dt, draw_orbits=True, orbit_stroke=0.7, planet_scaler=2, planet_min=5, planet_max=15):
    
    if draw_orbits:
      for planet in solarsystem.planets:
        orbit = solarsystem.get_orbit(planet.eph, dt, dt + datetime.timedelta(days = planet.year))
        self.draw_orbit(orbit, stroke=orbit_stroke)
    
    for planet in solarsystem.planets:
      position = solarsystem.position(planet.eph, dt)
      size = planet.radius*planet_scaler
      if size < planet_min: size = planet_min
      if size > planet_max: size = planet_max
      self.draw_object(position, size, planet.color, 1)
    
    self.draw_object((0,0,0), planet_max+2, "#eaff2e", 1)

  def draw_ephemobject(self, obj, dt, size=0.7, label_size=7, label=None, label_offset=10):
    position = solarsystem.position(obj, dt)
    self.draw_object(position, size, "#ffffff", 1)
    
    if label != None:
      self.draw_label(position, label, "#dddddd", label_size, label_offset=10)
  
  
  def write(self, filename):
    handle = open(filename, 'w')
    
    self.document += "\n</svg>"
    
    handle.write(self.document)
    handle.close()
    
