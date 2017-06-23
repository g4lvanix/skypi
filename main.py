#!/usr/bin/env python3

import ephem
import numpy as np
import heapq

# location info
qth_lat = 51.1333
qth_lon = 13.75
qth_el= 232.0

# satellites to display information about
qth_watchlist = ["ISS","AO-85","SO-50"]

def locationSetup(lat,lon,el=0,p=0,horz=0):
	obs = ephem.Observer()
	obs.lat = np.deg2rad(lat)
	obs.lon = np.deg2rad(lon)
	obs.elevation = el
	obs.pressure = p
	obs.horizon = np.deg2rad(horz)
	return obs


def readTLE(fname):
	sats = []
	with open(fname,'r') as f:
		tles = f.readlines()
		
		for i in range(0,len(tles)-2,3):
			sats.append(ephem.readtle(tles[i],tles[i+1],tles[i+2]))

	return sats

def extractWatchlist(sats,watchlist):
	watched = []
	# get the satellite names
	for s in sats:
		if watchlist.__contains__(s.name):
			watched.append(s)

	return watched


if __name__ == "__main__":
	qth = locationSetup(qth_lat,qth_lon,qth_el)
	sats = readTLE("stations.txt")
	wl = extractWatchlist(sats,qth_watchlist)

	for w in wl:
		rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = qth.next_pass(w)

		print(w.name,"Rise time: %s  Rise Az: %03.1f\nMax alt. time: %s Max. alt.: %03.1f\nSet time: %s Set Az: %03.1f\n" % (rise_time,np.rad2deg(rise_az),
		max_alt_time,np.rad2deg(max_alt),set_time,np.rad2deg(set_az)) )

	#while True:



'''
with open('stations.txt','r') as f:
	zarya = ephem.readtle(f.readline(),f.readline(),f.readline())

qth = locationSetup(qth_lat,qth_lon,qth_el)

for i in range(3):

	rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = qth.next_pass(zarya)
	qth.date = max_alt_time
	zarya.compute(qth)

	print("Rise time: %s  Rise Az: %03.1f\n\
Max alt. time: %s Max alt. Az: %03.1f Max. El.: %03.1f\n\
Set time: %s Set Az: %03.1f\n" % (rise_time,np.rad2deg(rise_az),
max_alt_time,np.rad2deg(zarya.az),np.rad2deg(max_alt),set_time,np.rad2deg(set_az)) )

	qth.date = set_time
'''
