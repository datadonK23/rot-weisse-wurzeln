#!/usr/bin/python
""" create_map

Creates map of POIs.

Author: datadonk23
Date: 14.04.19 
"""

import os, base64
import geopandas as gpd
import folium

# Basemap
m = folium.Map(location=[48.04274, 14.42127], zoom_start=15,
               tiles="Stamen Toner")


# Data
path = "data/"
f_name = "locations.geojson"
f_path = os.path.join(path, f_name)

gdf = gpd.read_file(f_path)


# Mark POIs
for _, row in gdf.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        tooltip=row["name"],
        popup=folium.Popup(folium.IFrame("<img src='data:image/jpeg;base64,{}'>".format(base64.b64encode(open(row["photo_url"], "rb").read()).decode()),
width=350, height=250), max_width=500),
        icon=folium.Icon(color="red", prefix="fa", icon="futbol-o")
    ).add_to(m) #FIXME heder, text


# Save map
m.save("index.html")
