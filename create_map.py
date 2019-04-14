#!/usr/bin/python
""" create_map

Creates map of POIs.

Author: datadonk23
Date: 14.04.19 
"""

import folium

# Basemap
m = folium.Map(location=[48.04274, 14.42127], zoom_start=15)

# Mark POIs
folium.Marker(
    location=[48.04274, 14.42127],
    popup="Info",
    icon=folium.Icon(color="red", prefix="fa", icon="futbol-o")
).add_to(m) #FIXME

# Save map
m.save("index.html")
