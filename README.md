# Mapping Vancouver's Housing Affordability Crisis

Vancouver Housing Maps: creating a Python and matplotlib-based platform for mapping Canadian census data. Example usage for this project involved using 2011 National Housing Survey data from Statistics Canada to map different housing affordability data points across different regions in the Metro Vancouver area.

## Examples

![Figure 1: Housing affordability.](images/affordability.png?raw=true)

![Figure 2: Median rents.](images/rents.png?raw=true)

For more examples, see pdf-output/.

## Description of files
   README - this file, an overview of the project
   Contract.pdf - project proposal

   shp.py - the *main file*, this includes the Dataplot class, a set of tools to 
            draw shapefile data, parse and bind geographically sorted data, and 
            plot using matplotlib.

   dataFilter.py - uses Pandas to filter large xlsx/csv files by keywords.
   vanData.py - reads metadata.csv to iterate through several pre-prepared
                metrics from census data in Vancouver.

   metadata.csv - instructions for vanData.py, points to spreadsheets and
                  gives titles and descriptions
   
   Affordability.pdf - sample output, colour-based map of Vancouver housing data
   Results/ - 6 different maps of different data points generated with vanData.py
   Data/ - geographical shapefiles and census data

## Additional modules required by this software: 
   pillow, matplotlib, requests, numpy, pyshp, shapely, descartes, pandas, xlrd, xlwt

## Demonstrable accomplishments of this project:
	- Created tools to be able to (generically):
		- Filter through large datasets for relevant information
		- Parse through data in spreadsheet and GIS shapefile formats
		- Bind this data using keyword identifiers
		- Present data graphically in a ‘choropleth map’ (colours shaded
		  proportionally to data)
	- Used these tools to:
		- Process large Canadian census data files for relevant info
		- Display demographic metrics for several data points from the
		  2011 National Housing Survey

## Usage instructions: 
  Run shp.py or vanData.py.

## Additional comments:
	Some work manipulating the shapefile and the data was done outside of Python,
	 - the .shp format was particularly difficult to modify in Python and I ended 
	up using external software (mapshaper) to filter it for the relevant region. 
	While the software itself is capable of processing larger regions, processing
	power limits proved prohibitive.

(c) Jason Liu 2017.
