#!/usr/bin/env python3

from math import atan2, cos, radians, sin, sqrt
import json, sys

# calculate the distance between two lat/lons
def distance(lat_lon1, lat_lon2):
	lat1 = radians(lat_lon1[0])
	lon1 = radians(lat_lon1[1])
	lat2 = radians(lat_lon2[0])
	lon2 = radians(lat_lon2[1])

	R = 6373 # km
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))
	return R * c * 1000 # meters

# read and store crimes from json file
def read_crimes(crime_db):
	with open(crime_db) as json_file:
		json_data = json.load(json_file)

	clean_data = []
	for item in json_data['data']:
		lat_lon = tuple(map(float, item[27][1:3]))
		item = {'id': item[8], 'lat_lon': lat_lon}
		if item['id']: # some crimes have no id
			clean_data.append(item)

	return clean_data

# find all crimes within distance
def find_crimes(crimes, start, radius):
	local_crimes = []
	for crime in crimes:
		lat_lon = crime['lat_lon']
		d = distance(start, lat_lon)
		if abs(d) < radius:
			local_crimes.append((crime['id'], d))
	return local_crimes

if __name__ == '__main__':
	try: # parse input
		dbfile = sys.argv[1]
		lat = float(sys.argv[2])
		lon = float(sys.argv[3])
		d = int(sys.argv[4])
	except:
		print('ERROR: arguments should be <FILE> <LAT> <LONG> <DIST>')
	else: # calculate
		crimes = read_crimes(dbfile)
		local_crimes = find_crimes(crimes, [lat, lon], d)
		local_crimes = sorted(local_crimes, key=lambda x: x[1])
		for crime in local_crimes:
			print('%s: %d' % (crime[0], crime[1]))
