#!/usr/bin/env python
import drawing
import datetime
import solarsystem
import json
import ephem
import parse

svg = drawing.DrawSVG(800,800, 7)

now = datetime.datetime.utcnow()
svg.draw_solarsystem(now)


data   = json.loads(open("/home/natronics/Code/Astrobot/data/spacecraft.json", 'r').read())

# MSL
msl    = solarsystem.make_ephem_object(data['msl'])

msl_launch = datetime.datetime(2011,11,26,15,2,0)
msl_arrive = datetime.datetime.strptime(data['msl']['arrival_date'], "%Y-%m-%dT%H:%M:%S")

orbit_past = solarsystem.get_orbit(msl, msl_launch, now, steps=20)
svg.draw_orbit(orbit_past, color="#999999")

orbit_future = solarsystem.get_orbit(msl, now, msl_arrive)
svg.draw_orbit(orbit_future,color="#999999",  alpha=0.4, dashed=True)

svg.draw_ephemobject(msl, now, label="MSL")

# Juno
juno    = solarsystem.make_ephem_object(data['juno'])
juno_launch = datetime.datetime(2011,8,5,16,25,0)
juno_arrive = datetime.datetime.strptime(data['juno']['arrival_date'], "%Y-%m-%dT%H:%M:%S")

orbit_past_h = parse.get_orbit("juno.txt", juno_launch, now)
svg.draw_orbit(orbit_past_h, color="#aa9999", alpha=0.4)

orbit_future_h = parse.get_orbit("juno.txt", now, juno_arrive)
svg.draw_orbit(orbit_future_h, color="#aa9999", alpha=0.4, dashed=True)

#orbit_past = solarsystem.get_orbit(juno, juno_launch, now)
#svg.draw_orbit(orbit_past, color="#aa9999", alpha=0.4)

svg.draw_ephemobject(juno, now, label="Juno")

svg.draw_label((3,796), now.strftime("%A %B %d, %Y %H:%M UTC"), "#999999", 11, screen=True)

svg.write("solarsystemnow.svg")


p = solarsystem.position(ephem.Sun(), now)


png = drawing.DrawPNG(1280,720, 5, center=(p[0],p[1]))

#png.draw_object((0,0), 7, (0.4,0.4,0.1), 0.8)

png.draw_solarsystem(now, orbit_stroke=1.2, planet_scaler=1.5, planet_min=2, planet_max=7)

msl    = solarsystem.make_ephem_object(data['msl'])

msl_launch = datetime.datetime(2011,11,26,15,2,0)
msl_arrive = datetime.datetime.strptime(data['msl']['arrival_date'], "%Y-%m-%dT%H:%M:%S")

orbit_past = solarsystem.get_orbit(msl, msl_launch, now, steps=40)
png.draw_line(orbit_past, 1, (0.6,0.6,0.6))

png.draw_ephemobject(msl, now, label="MSL", label_size=8.2, label_offset=3)

png.write("solarsystemnow.png")


