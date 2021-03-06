#!/usr/bin/python
""" create_map

Creates map of POIs.

Author: datadonk23
Date: 14.04.19 
"""

import os, json
from typing import List, NewType
import geopandas as gpd # type: ignore
import folium # type: ignore
from folium import FeatureGroup
from locate_control import LocateControl
import validators # type:ignore


# Custom types
Html = NewType("Html", str)


# Color constants
RED: str = "#d90000"
WHITE: str = "#fffff0" # ivory
GREEN: str = "#00ff00" # lime


# Basemap
map_center: List[float] = [48.04274, 14.42127]
map: folium.Map = folium.Map(location=map_center, zoom_start=15, tiles=None)

folium.TileLayer(tiles="http://tile.stamen.com/toner-background/{z}/{x}/{y}.png",
                 attr="style:"
                      "<a href=http://maps.stamen.com/toner-background/>Stamen "
                      "toner-background</a> | "
                      "<a href=imprint.html>Impressum</a>",
                 name="Basiskarte", show=True).add_to(map)


# Add location tracker
LocateControl(
    strings={"title": "Wo bin ich?", "popup": "Du bist hier"},
    keepCurrentZoomLevel=True
).add_to(map)


# Data imports
path: str = "data/"
f_name_points: str = "locations.geojson"
f_path_points: str = os.path.join(path, f_name_points)

points_gdf: gpd.GeoDataFrame = gpd.read_file(f_path_points)

f_name_grounds: str = "grounds.geojson"
grounds_ref: str = os.path.join(path, f_name_grounds)

walks: dict = {}
f_name_walks: str = "walks.geojson"
f_path_walks: str = os.path.join(path, f_name_walks)
with open(f_path_walks) as f:
    walks_data = json.load(f)
for feature in walks_data["features"]:
    raw_coords: List[List[float]] = feature["geometry"]["coordinates"][0]
    coords: List[List[float]] = [[coord[1], coord[0]] for coord in raw_coords]
    walks[feature["properties"]["name"]] = coords


# Grounds feature
folium.GeoJson(
    grounds_ref,
    name="Spielstätten",
    style_function= lambda feature: {
        "fillColor": GREEN,
        "color": WHITE,
        "weight": 1,
        "fillOpacity": 0.5
        },
    tooltip=folium.GeoJsonTooltip(fields=["name"], labels=False),
    show=False
).add_to(map)


# Walks feature
fg_walks: FeatureGroup = FeatureGroup(name="Rundgänge", show=True)

for walk_id, walk_coords in walks.items():
    # Walk feature
    loc: List[List[float]] = walk_coords

    folium.PolyLine(
        locations=loc,
        tooltip="Rundgang " + walk_id,
        color=RED,
        weight=6,
        opacity=0.75,
        smooth_factor=1,
    ).add_to(fg_walks)

    # Start of walk
    start_loc: List[float] = loc[0]

    folium.RegularPolygonMarker(
        location=start_loc,
        number_of_sides=3,
        color=RED,
        fill_color=RED,
        fill_opacity=1,
        rotation=195,
        radius=12
    ).add_to(fg_walks)

fg_walks.add_to(map)


# Render information
def get_info(title: str, description: str, photo_url: str, link: str) -> Html:
    """ Generates HTML code for popup

    :param title: title text
    :param description: description text < 1001 characters
    :param photo_url: url of photo (max_width=300px, height=200px)
    :param link: url for external info page
    :return: HTML code snippet
    """

    # Input validation
    if len(title) > 40:
        raise ValueError("Title string is too long")
    if len(description) > 1000:
        raise ValueError("Description string is too long")
    if len(link) > 150:
        raise ValueError("URL for external page too long")
    if not validators.url(link):
        raise ValueError("URL for external page is malformed")
    if not ((".jpg" in photo_url) or (".png" in photo_url)):
        raise ValueError("Photo URL must point to a .jpg or .png file")

    html = Html(""" 
    <!doctype html>
    <html>
    <h1>{}</h1>""".format(title) + """
    <iframe width="284" height="184" src='{}'""".format(photo_url) + """ 
    frameborder="0"></iframe>
    <p>{}</p>""".format(description) +
    """<button onclick="window.open('{}','_blank')" type="button">
         Mehr dazu</button>""".format(link) + """
    </html>""")

    return html


# Mark POIs
fg_points: FeatureGroup = FeatureGroup(name="Stationen", show=True)

for _, row in points_gdf.iterrows():
    iframe = folium.Html(get_info(row["name"], row["text"],
                                  row["photo_url"], row["link"]), script=True)
    popup = folium.Popup(iframe, parse_html=True, max_width=280)

    loc = [row.geometry.y, row.geometry.x]
    folium.Marker(
        location=loc,
        tooltip=row["name"], popup=popup,
        icon=folium.Icon(color=RED, prefix="fa", icon="futbol-o")
    ).add_to(fg_points)

fg_points.add_to(map)


# Layercontrol
folium.LayerControl().add_to(map)

# Save map
map.save("index.html")
