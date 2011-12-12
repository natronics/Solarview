#!/usr/bin/env python
import datetime
import ephem

def get_orbit(filename, begin, end):
  orbit = readfile(filename)
  
  orbit_line = []
  
  for o in orbit:
    d = o[0]
    if d >= begin and d <= end:
      orbit_line.append((o[1],o[2]))

  return orbit_line

def readfile(f):
  f_in = open(f, 'r')
  read = False
  dates = []
  orbit = []
  for line in f_in:
    if line[0:5] == '$$EOE':
      break
    if read:
      li = line.split(',')
      
      dt = ephem.date(float(li[0]) - 2415020).datetime()
      x  =            float(li[2])
      y  =            float(li[3])
      z  =            float(li[4])
      
      #dates.append(dt)
      orbit.append((dt, x, y, z))
      
    if line[0:5] == '$$SOE':
      read = True
    
  return orbit


"""
orbit = get_orbit(datetime.datetime(2013,2,15), datetime.datetime(2013,3,1))

for o in orbit:
  print o
"""
