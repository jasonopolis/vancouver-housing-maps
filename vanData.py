#!/usr/bin/env python3
# (c) 2017 Jason Liu
"""Iterates through entries in metadata.csv, and plots data using Dataplots."""

import csv
from shp import *

with open('metadata.csv') as f:
	csvr = csv.reader(f)
	for row in csvr:
		if row[2] == 'dataID':
			continue
		van = Dataplot(sf = row[0], coordinates = (float(row[8]), float(row[9]), float(row[10]), float(row[11])), dataset = row[1])
		van.parseData(dataID = row[2], data = row[3])
		van.mapPlot(shpID = row[4], title = row[5], desc = row[6])
		van.save(filename = row[7])