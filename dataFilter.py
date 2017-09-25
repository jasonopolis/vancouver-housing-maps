#!/usr/bin/env python3
# (c) 2017 Jason Liu
"""Quick script to filter large CSV files using a Pandas dataframe (for speed and memory efficency)."""

from sys import argv
import pandas as pd

filepath = str(argv[1]) if len(argv) > 1 else 'bc2011nhs.csv'
columnname = str(argv[2]) if len(argv) > 2 else 'CD_Name'
filtername = str(argv[3]) if len(argv) > 3 else 'Greater Vancouver'
outfilepath = str(argv[4]) if len(argv) > 4 else 'GV2011nhs.csv'

if filepath.endswith("xlsx"):
			file = pd.read_excel('Data/'+filepath)
elif filepath.endswith("csv"):
			file = pd.read_csv('Data/'+filepath)

newfile = file[file[columnname].isin([filtername])]

if filepath.endswith("xlsx"):
			newfile.to_excel('Data/'+outfilepath)
elif filepath.endswith("csv"):
			newfile.to_csv('Data/'+outfilepath)

print(newfile.head())