#!/usr/bin/env python
import json
import datetime
from data import horizons
import config
import time

origin = datetime.datetime(1970,1,1,0,0,0)

data = {}

def get_spacecrat_data(key, craft):
  h = horizons.Horizons()

  start = origin + datetime.timedelta(seconds=craft["start"])
  end   = origin + datetime.timedelta(seconds=craft["end"])

  print "Getting data for", key
  
  orbit_data = h.get_track(craft["code"], start, end)

  print "Got data for", key
  
  time.sleep(5)
  
  data[key] = {"orbit": orbit_data}

for key in config.spacecraft:
  #print config.spacecraft[key]
  get_spacecrat_data(key, config.spacecraft[key])

f_out = open(config.datafile,'w')
f_out.write(json.dumps(data))
f_out.close()
