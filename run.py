#!/usr/bin/env python
import drawing
import datetime
import solarsystem
import json
import ephem

now = datetime.datetime.utcnow()


p = solarsystem.position(ephem.Sun(), now)
png = drawing.DrawPNG(1280,720, 5, center=(p[0],p[1]))

png.draw_solarsystem(now, orbit_stroke=1.2, planet_scaler=1.5, planet_min=2, planet_max=7)


#png.draw_line(orbit_past, 1, (0.6,0.6,0.6))

spacecraft = solarsystem.spacecraft()

msl = spacecraft.get_location("msl", now)

png.draw_object(msl, 3, (0.9,0.9,0.9), 1)

png.write("solarsystemnow.png")
