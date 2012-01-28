#!/usr/bin/env python
import json
import datetime
from data import horizons
import config
import time
import sys

origin = datetime.datetime(1970,1,1,0,0,0)

def get_spacecrat_data(key, craft):

  data = {}
  
  h = horizons.Horizons()

  start = origin + datetime.timedelta(seconds=craft["start"])
  end   = origin + datetime.timedelta(seconds=craft["end"])

  print "Getting data for", key
  
  orbit_data = h.get_track(craft["code"], start, end)

  time.sleep(5)
  
  data[key] = {"orbit": orbit_data}
  
  f_out = open("data/" + key + ".json",'w')
  f_out.write(json.dumps(data))
  f_out.close()
  
  print "Got data for", key

def get_all():
  for key in config.spacecraft:
    get_spacecrat_data(key, config.spacecraft[key])

def get_spacecraft(key):
  get_spacecrat_data(key, config.spacecraft[key])


if len(sys.argv) > 0:
  get_spacecraft(sys.argv[1])
else:
  get_all()
