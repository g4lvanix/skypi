#!/usr/bin/env python3

import ephem
import numpy as np
import urllib.request
import shutil

# TLE URL
tle_url = "http://www.amsat.org/amsat/ftp/keps/current/nasabare.txt"
# location info
qth_lat = 51.1333
qth_lon = 13.75
qth_el= 232.0

# satellites to display information about
qth_watchlist = ["ISS","AO-85","SO-50"]

# sets up the ephem Observer for the current location
def locationSetup(lat,lon,el=0,p=0,horz=0):
	obs = ephem.Observer()
	obs.lat = np.deg2rad(lat)
	obs.lon = np.deg2rad(lon)
	obs.elevation = el
	obs.pressure = p
	obs.horizon = np.deg2rad(horz)
	return obs

# updates the TLE file from the AMSAT server
def updateTLE(url):
	with urllib.request.urlopen(url) as resp, open("stations.txt","wb") as f:
		shutil.copyfileobj(resp,f)

# reads a standard celestrak TLE file (needs to be stripped of any non TLE headers)
def readTLE(fname):
	with open(fname,'r') as f:
		tles = f.readlines()
		sats = [ephem.readtle(tles[i],tles[i+1],tles[i+2]) for i in range(0,len(tles)-2,3)]

	return sats

# returns a list of ephem.EarthSatellite objects whose names correspond
# to the strings in watchlist
def extractWatchlist(sats,watchlist):
	# get the satellite names
	# so pythonic! :P
	watched = [s for s in sats if s.name in watchlist]
	return watched

# deals with getting more info for a satellite pass than next_pass will provide
# such as max. altitude azimuth
def getPassInfo(obs,sat):
	dummy = obs
	max_alt = 0
	while max_alt < np.deg2rad(5):
		rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = dummy.next_pass(sat)
		dummy.date = dummy.date + 30*ephem.minute

	dummy_date = max_alt_time
	sat.compute(dummy)

	return (rise_time, rise_az, max_alt_time, sat.az, max_alt, set_time, set_az)


if __name__ == "__main__":
	qth = locationSetup(qth_lat,qth_lon,qth_el)
	sats = readTLE("stations.txt")
	wl = extractWatchlist(sats,qth_watchlist)

	for w in wl:
		pi = getPassInfo(qth,w)

		print(w.name,"\nRise time: %s  Rise Az: %03.1f\nMax alt. time: %s Max alt. Az: %03.1f Max. Alt.: %03.1f\nSet time: %s Set Az: %03.1f\n" % (pi[0],np.rad2deg(pi[1]), pi[2],np.rad2deg(pi[3]),np.rad2deg(pi[4]),pi[5],np.rad2deg(pi[6])) )

	#while True:
