#!/usr/bin/env python
import json
import datetime
from data import horizons
import config

origin = datetime.datetime(1970,1,1,0,0,0)

data = {}

h = horizons.Horizons()

start = datetime.datetime(2011,11,26,16,0,0)
#end   = datetime.datetime(2011,11,30,16,0,0)
end   = datetime.datetime(2012, 8, 5, 0,0,0)

msl = h.get_track('-76', start, end)

start_u = start - origin
start_u = int((start_u.days * 86400) + start_u.seconds)
end_u = end - origin
end_u = int((end_u.days * 86400) + end_u.seconds)

data["msl"] = {"orbit": msl, "start": start_u, "end": end_u}

f_out = open(config.datafile,'w')
f_out.write(json.dumps(data))
f_out.close()
