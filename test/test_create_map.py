#!/usr/bin/python
""" test_create_map

Author: datadonk23
Date: 30.04.19 
"""

import unittest
from hypothesis import given
import hypothesis.strategies as st

import geopandas as gpd

from create_map import map_center, loc, points_gdf, grounds_ref, get_info


class TestLocation(unittest.TestCase):
    def test_map_center_size(self):
        center = map_center
        self.assertEqual(len(center), 2,
                         "Incorrect number of coordinates in map_center")

    def test_loc_size(self):
        locaction = loc
        self.assertEqual(len(locaction), 2,
                         "Incorrect number of coordinates in loc")

    def test_map_center_bb(self):
        center = map_center
        lat_max = 48.0875
        lat_min = 48.0232
        long_max = 14.4717
        long_min = 14.3765
        self.assertTrue(lat_min <= center[0] <= lat_max,
                        "Lat of map center not within city boundaries")
        self.assertTrue(long_min <= center[1] <= long_max,
                        "Long of map center not within city boundaries")


class TestPointData(unittest.TestCase):
    def setUp(self):
        self.data = points_gdf

    def test_size(self):
        self.assertEqual(self.data.shape[0], 10,
                         "Incorrect number of rows in point GDF")
        self.assertEqual(self.data.shape[1], 5,
                         "Incorrect number of cols in point GDF")

    def test_columns(self):
        exp_cols = ["id", "name", "photo_url", "text", "geometry"]
        cols = list(self.data.columns.values)
        self.assertEqual(cols, exp_cols,
                         "Incorrect column names in point GDF")

    def test_empty_fields(self):
        self.assertEqual(self.data.isna().sum().sum(), 0,
                         "There are missing empty fields in point GDF")

    def test_geometry(self):
        self.assertIsInstance(self.data.geometry, gpd.GeoSeries,
                              "Point GDF geometry type is not a GeoSeries")


class TestGroundsData(unittest.TestCase):
    def setUp(self):
        self.data = gpd.read_file(grounds_ref)

    def test_size(self):
        self.assertEqual(self.data.shape[0], 2, #FIXME 3
                         "Incorrect number of rows in grounds GEOJSON")
        self.assertEqual(self.data.shape[1], 3,
                         "Incorrect number of cols in grounds GEOJSON")

    def test_columns(self):
        exp_cols = ["id", "name", "geometry"]
        cols = list(self.data.columns.values)
        self.assertEqual(cols, exp_cols,
                         "Incorrect column names in grounds GEOJSON")

    def test_empty_fields(self):
        self.assertEqual(self.data.isna().sum().sum(), 0,
                         "There are missing empty fields in grounds GEOJSON")

    def test_geometry(self):
        data = points_gdf
        self.assertIsInstance(data.geometry, gpd.GeoSeries,
                              "Invalid geometry in grounds GEOJSON")


class TestGetInfo(unittest.TestCase):
    def test_is_html(self):
        info = get_info("title", "descr", "url.jpg")
        self.assertIn("<html>", info, "No html start tag in info")
        self.assertIn("</html>", info, "No html closing tag in info")

    @given(test_title=st.text(max_size=40))
    def test_contains_title(self, test_title):
        info = get_info(test_title, "descr", "url.png")
        self.assertIn("<h1>" + test_title + "</h1>", info,
                      "Test tile not in info")

    @given(test_descr=st.text(max_size=1000))
    def test_contains_description(self, test_descr):
        info = get_info("title", test_descr, "url.jpg")
        self.assertIn("<p>" + test_descr + "</p>", info,
                      "Test description not in info")

    def test_contains_url(self):
        test_url = "data\/photos\/v_platz.jpg"
        info = get_info("title", "descr", test_url)
        self.assertIn("src='" + test_url + "'", info,
                      "Test URL not in info")

    @given(test_title=st.text(min_size=41))
    def test_max_len_title(self, test_title):
        self.assertRaises(ValueError, get_info, test_title, "descr", "url.png")

    def test_max_len_description(self):
        long_descr = "a" * 1001
        self.assertRaises(ValueError, get_info, "title", long_descr, "url.png")

    def test_format_url(self):
        self.assertRaises(ValueError, get_info, "title", "descr",
                          "data\/photos\/v_platz.txt")
        self.assertRaises(ValueError, get_info, "title", "descr",
                          "data\/photos\/v_platzjpg")


if __name__ == '__main__':
    unittest.main()
