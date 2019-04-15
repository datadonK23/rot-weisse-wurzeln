#!/usr/bin/python
""" create_map

Creates map of POIs.

Author: datadonk23
Date: 14.04.19 
"""

import os
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


# Render information
def get_info(title, description, photo_url):
    """ Generates HTML code for popup

    :param title:
    :param description: description text < 1001 characters
    :param photo_url: url of photo (max_width=300px, height=200px)
    :return: HTML code snippet
    """

    html = """ 
    <!doctype html>
    <html>
    <h1>{}</h1>""".format(title) + """
    <iframe width="300" height="200" src='{}'""".format(photo_url) + """ 
    frameborder="0"></iframe>
    <p>{}</p>""".format(description) + """
    </html>"""

    return html


# Mark POIs
for _, row in gdf.iterrows():
    iframe = folium.Html(get_info(row["name"], row["text"],
                                  row["photo_url"]), script=True)
    popup = folium.Popup(iframe, parse_html=True, max_width=500)

    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        tooltip=row["name"],
        popup=popup,
        icon=folium.Icon(color="red", prefix="fa", icon="futbol-o")
    ).add_to(m)


# Save map
m.save("index.html")
