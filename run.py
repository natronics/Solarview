#!/usr/bin/env python
import drawing
import datetime
import solarsystem
import json
import ephem
import config

now = datetime.datetime.utcnow()


p = solarsystem.position(ephem.Sun(), now)
png = drawing.DrawPNG(720,720, 1.8, center=(0,0))

png.draw_solarsystem(now, orbit_stroke=1.4, planet_scaler=3, planet_min=1.5, planet_max=7)

spacecraft = solarsystem.spacecraft()


for craft in config.spacecraft:
  #orbit_past = spacecraft.get_past_orbit(craft, now)
  #png.draw_line(orbit_past, 1, (0.6,0.6,0.6), 0.5)  
  scraft = spacecraft.get_location(craft, now)
  png.draw_object(scraft, 1, (0.95,0.95,0.95), 1)
  png.draw_text(scraft, config.spacecraft[craft]["label"], (0.95,0.95,0.95), 9, label_offset=5)

png.write("solarsystemnow.png")
