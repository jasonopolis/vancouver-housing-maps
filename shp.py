#!/usr/bin/env python3
# (c) 2017 Jason Liu
# Thanks to Professor Duane Bailey (cs.williams.edu/~bailey) for all the great stories, and thanks to the TAs for all the grading.
# Also thanks to Chris Havlin (chrishavlin.wordpress.com) for a very useful guide on plotting shapes in matplotlib.
"""Dataplot module, used for plotting choropleth (data-shaded colour) maps in matplotlib.  
If run on its own, demos functionality using Vancouver 2011 Stats Canada National Housing Survey data."""

import shapefile
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

__all__ = ['Dataplot']

class Dataplot(object):
	"""Generates a data-based colour-spectrum shape from inputs: 
		ESRI GIS shapefile filename/path (.shp, .dbf, .shx), 
		Window coordinates as tuple(west, south, east, north),
		Excel/CSV filename/path.
	Default values for Vancouver census subdivisions, dataset as StatsCan Census affordability data."""
	__slots__ = ["_sf", "_dataset", "_coord", "data"]

	def __init__(self, sf, coordinates, dataset):
		self._sf = sf
		self._coord = coordinates
		self._dataset = dataset

	@property
	def sf(self):
		"""Returns the input shapefile as a Python pyshp shapefile object."""
		return shapefile.Reader(self._sf)

	@property
	def coord(self):
		"""Returns the target coordinates as tuple(west, south, east, north)."""
		return self._coord

	@property
	def dataset(self):
		"""Returns path/filename of dataset file."""
		return self._dataset

	def parseData(self, dataID, data):
		"""Parses data as dict of identifier:value pairs and places into attribute Dataplot.data. 
		Takes arguments for column names in original file:
			dataID:	identifier column (e.g. region name, city name, region ID)
			data:	data column (numerical data only) """
		if self.dataset.endswith("xlsx"):
			file = pd.read_excel(self.dataset)
		elif self.dataset.endswith("csv"):
			file = pd.read_csv(self.dataset)
		else:
			raise Exception('Invalid file type specified. Initialize Dataplot object with dataset to a CSV or XLSX file.')

		# Sets NaN values in dataframe to None
		file = file.where((pd.notnull(file)), None)
		
		# Converts all items in id column to strings (for indexing)
		file[dataID] = file[dataID].astype(str)
		self.data = dict(file.set_index(dataID)[data])

	def properties(self):
		"""Returns some properties of the imported shapefile."""
		print('Number of shapes in shapefile:',len(self.sf.shapes()))
		print('Attributes of imported pyshp shapefile object:')
		for attrib in dir(self.sf.shapes()[0]):
			if not attrib.startswith('__'):
				print('	'+attrib)
		print('Fields in records (.dbf) of imported shapefile:')
		for field in self.sf.fields:
			if field[0] != "DeletionFlag":
				if field[1] == "C":
					print('	'+field[0]+"		(type Character)")
				elif field[1] == "N":
					print('	'+field[0]+"		(type Number)")
				elif field[1] == "L":
					print('	'+field[0]+"		(type Longs)")
				elif field[1] == "D":
					print('	'+field[0]+"		(type Dates)")
				else:
					print('	'+field[0]+"		(type Memo/other)")
	
	def mapPlot(self, shpID, title='', desc=''):
		"""Creates matplotlib plot for all shapes (and parts of shapes). Part of the code here is based off work by Chris Halvin (chrishavlin.wordpress.com).
		Takes arguments:
			shpID:	Relevant identifier label in shapefile metadata (.dbf)
			title:	Title of plot (optional)
			desc: 	Description of data interpretation
		Note: if the colour scale is incorrect, check data for unwanted zeroes instead of None/NaN."""
		fig = plt.figure()
		ax = plt.axes()
		
		# Correcting for the projection (in a slightly crude way but this developer lacks cartography knowledge).
		ax.set_aspect(1.35)

		# Takes shapefile fields to list, finds location in record of identifier
		fields = []
		for field in self.sf.fields:
			if field[0] != "DeletionFlag":
				fields.append(field[0])
		idIndex = fields.index(shpID)

		# Finds min and max of values for colouring
		dataValues = [x for x in list(self.data.values()) if x is not None]
		minDV = min(dataValues)
		maxDV = max(dataValues)
		rangeDV = maxDV - minDV

		for item in list(self.sf.iterShapeRecords()):
			shp, rec = item.shape, item.record

			recId = rec[idIndex]
			if recId in self.data:
				dataValue = self.data[recId]

				if dataValue is not None:
					# Converts value to index from 0-1 based on max and min
					indexColour = ((dataValue - minDV) / rangeDV)
					R, G, B = indexColour/3, indexColour/1.5, indexColour

			else:
				# Display for no data/data is None
				R, G, B = 1, 1, 1

			# For single-part shapes
			if len(shp.parts) == 1:
				shape = PolygonPatch(Polygon(shp.points), facecolor=[R,G,B], alpha = 1.0, zorder = 2)
				ax.add_patch(shape)
				
			# For multi-part shapes
			else:
				for i in range(len(shp.parts)):
					firstPart = shp.parts[i]
					if i < len(shp.parts) - 1:
						lastPart = shp.parts[i+1] - 1
					else:
						lastPart = len(shp.points)
					
					shape = PolygonPatch(Polygon(shp.points[firstPart:lastPart + 1]), facecolor=[R,G,B], alpha = 1.0, zorder = 2)
					ax.add_patch(shape)

		west, south, east, north = self.coord
		plt.xlim(west,east)
		plt.ylim(south,north)

		plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
		plt.title(title, fontsize=14, fontweight='bold')

		# Colourbar plotting
		cbax = fig.add_axes([0.21, 0.12, 0.6, 0.02])
		cdict = {'red': ((0.0, 0.0, 0.0), (1.0, 0.33, 0.33)),
		'green': ((0.0, 0.0, 0.0), (1.0, 0.67, 0.67)),
		'blue': ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0))}
		cmap = mpl.colors.LinearSegmentedColormap('PaleBlue',cdict,128)
		norm = mpl.colors.Normalize(vmin=(minDV), vmax=(maxDV))
		cb = mpl.colorbar.ColorbarBase(cbax, cmap=cmap,
                                norm=norm,
                                orientation='horizontal')
		cbax.tick_params(axis='both')
		cb.set_label(desc, fontsize=10)


	def save(self, filename = "Dataplot.pdf", type = 'pdf', dpi = 1200):
		"""Saves plot to file, given filename."""
		plt.savefig(filename = filename, format = type, dpi = dpi)
		print("Plot saved to "+filename)


if __name__ == "__main__":
	print("Demo: Vancouver Housing Affordability, map files and data courtesy of Statistics Canada.")
	van = Dataplot(sf = 'Data/van-csd11/van-csd11', coordinates = (-123.30, 49.04, -122.54, 49.41), dataset = "Data/2011census/sheltercosts.xlsx")
	van.properties()
	van.parseData(dataID = 'CSDUID', data = 'Total')
	van.mapPlot(shpID = 'CSDUID', title ='Vancouver Housing Affordability, 2011', desc = '% of households spending more than 30% of income on housing')
	van.save(filename = "Affordability.pdf")