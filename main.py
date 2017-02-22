#!/usr/bin/env python3

import ephem
import numpy as np

qth = ephem.Observer()
qth.lat = np.deg2rad(51.1333)
qth.lon = np.deg2rad(13.75)
qth.elevation = 232.0
qth.pressure = 0
#qth.horizon = np.deg2rad(15.0)

with open('stations.txt','r') as f:
	zarya = ephem.readtle(f.readline(),f.readline(),f.readline())


for i in range(3):

	rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = qth.next_pass(zarya)
	qth.date = max_alt_time
	zarya.compute(qth)

	print("Rise time: %s  Rise Az: %03.1f\n\
Max alt. time: %s Max alt. Az: %03.1f Max. El.: %03.1f\n\
Set time: %s Set Az: %03.1f\n" % (rise_time,np.rad2deg(rise_az),
max_alt_time,np.rad2deg(zarya.az),np.rad2deg(max_alt),set_time,np.rad2deg(set_az)) )

	qth.date = set_time
