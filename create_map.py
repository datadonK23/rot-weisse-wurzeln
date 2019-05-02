#!/usr/bin/python
""" create_map

Creates map of POIs.

Author: datadonk23
Date: 14.04.19 
"""

import os
from typing import List, NewType
import geopandas as gpd # type: ignore
import folium # type: ignore
from locate_control import LocateControl


# Custom types
Html = NewType("Html", str)


# Basemap
map_center: List[float] = [48.04274, 14.42127]
m = folium.Map(location=map_center, zoom_start=15,
               tiles="http://tile.stamen.com/toner-background/{z}/{x}/{y}.png",
               attr="style:<a "
                    "href=http://maps.stamen.com/toner-background/>Stamen "
                    "toner-background</a> | <a href=imprint.html>Impressum</a>"
               )


# Add location tracker
LocateControl(
    strings={"title": "Wo bin ich?", "popup": "Du bist hier"},
    keepCurrentZoomLevel=True
).add_to(m)


# Data
path = "data/"
f_name = "locations.geojson"
f_path = os.path.join(path, f_name)

gdf: gpd.GeoDataFrame = gpd.read_file(f_path)


# Render information
def get_info(title: str, description: str, photo_url: str) -> Html:
    """ Generates HTML code for popup

    :param title: title text
    :param description: description text < 1001 characters
    :param photo_url: url of photo (max_width=300px, height=200px)
    :return: HTML code snippet
    """

    if len(title) > 40:
        raise ValueError("Title string is too long")
    if len(description) > 1000:
        raise ValueError("Description string is too long")
    if (".jpg" in photo_url) or (".png" in photo_url):
        pass
    else:
        raise ValueError("Photo URL must point to a .jpg or .png file")


    html = Html(""" 
    <!doctype html>
    <html>
    <h1>{}</h1>""".format(title) + """
    <iframe width="310" height="210" src='{}'""".format(photo_url) + """ 
    frameborder="0"></iframe>
    <p>{}</p>""".format(description) + """
    </html>""")

    return html


# Mark POIs
for _, row in gdf.iterrows():
    iframe = folium.Html(get_info(row["name"], row["text"],
                                  row["photo_url"]), script=True)
    popup = folium.Popup(iframe, parse_html=True, max_width=350)

    loc = [row.geometry.y, row.geometry.x]
    folium.Marker(
        location=loc,
        tooltip=row["name"], popup=popup,
        icon=folium.Icon(color="red", prefix="fa", icon="futbol-o")
    ).add_to(m)


# Save map
m.save("index.html")
