#!/usr/bin/env python3
# (c) 2017 Jason Liu
"""Experimental: using Folium to represent data in an interactive web interface."""

import pandas as pd
import folium
from folium import plugins
from branca.colormap import linear


van = folium.Map(
	location=[49.249172, -123.024681],
	tiles = 'Stamen Toner',
	zoom_start=11)

income = pd.read_excel('Data/2011census/visibleminorityratio.xlsx')

van.choropleth(
    geo_path='Data/van-csd11.json',
    data=income,
    columns = ['CSDUID', 'Total'],
    key_on='feature.properties.CSDUID',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Visible Minority Ratio (%)',
    highlight=True,
    reset=True
)

folium.LayerControl().add_to(van)

plugins.Fullscreen(
    position='topright',
    title='Expand me',
    titleCancel='Exit me',
    forceSeparateButton=True).add_to(van)

van.save('van.html')