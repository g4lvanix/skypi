#!/usr/bin/env python3

import ephem
import numpy as np 

qth = ephem.Observer()
qth.lat, qth.lon = 51.0209, 13.70844
#qth.pressure = 0


with open('stations.txt','r') as f:
	zarya = ephem.readtle(f.readline(),f.readline(),f.readline())

info = qth.next_pass(zarya)
print("Rise time: %s Az: %s\n\
Max alt. time: %s Max alt. Az: %s\n\
Set time: %s Set Az: %s\n" % (info[0],info[1]*180/np.pi,info[2],info[3]*180/np.pi,info[4],info[5]*180/np.pi) )
