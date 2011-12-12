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

svg.draw_ephemobject(msl, now, "MSL")

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

svg.draw_ephemobject(juno, now, "Juno")

svg.draw_label((3,796), now.strftime("%A %B %d, %Y %H:%M UTC"), "#999999", 11, screen=True)

svg.write("solarsystemnow.svg")
