#!/usr/bin/python
""" test_data

Author: datadonk23
Date: 06.09.19 
"""

import unittest
import validators, mimetypes

import geopandas as gpd

from create_map import points_gdf, grounds_ref, walks


class TestPointData(unittest.TestCase):
    def setUp(self):
        self.data = points_gdf

    def test_size(self):
        self.assertEqual(self.data.shape[0], 9,
                         "Incorrect number of rows in point GDF")
        self.assertEqual(self.data.shape[1], 6,
                         "Incorrect number of cols in point GDF")

    def test_columns(self):
        exp_cols = ["id", "name", "photo_url", "text", "link", "geometry"]
        cols = list(self.data.columns.values)
        self.assertEqual(cols, exp_cols,
                         "Incorrect column names in point GDF")

    def test_empty_fields(self):
        self.assertEqual(self.data.isna().sum().sum(), 0,
                         "There are missing empty fields in point GDF")

    def test_photo_url(self):
        for _, url in self.data.photo_url.iteritems():
            mimetype, _ = mimetypes.guess_type(url)
            self.assertTrue((mimetype and mimetype.startswith("image")),
                            "Photo is not an image in point GDF")

    def test_link(self):
        for _, url in self.data.link.iteritems():
            self.assertTrue(validators.url(url, public=True),
                            "Malformed link in point GDF")

    def test_geometry(self):
        self.assertIsInstance(self.data.geometry, gpd.GeoSeries,
                              "Point GDF geometry type is not a GeoSeries")


class TestGroundsData(unittest.TestCase):
    def setUp(self):
        self.data = gpd.read_file(grounds_ref)

    def test_size(self):
        self.assertEqual(self.data.shape[0], 5,
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


class TestWalksData(unittest.TestCase):
    def setUp(self):
        self.data = walks

    def test_size(self):
        self.assertTrue(bool(self.data), "Walks dict is empty")
        self.assertEqual(len(self.data), 1,
                         "Incorrect number of items in walks data")

    def test_empty_fields(self):
        for k, v in self.data.items():
            self.assertTrue(k, "Walks name is empty")
            self.assertTrue(v, "Walks coords are empty")

    def test_line_coords(self):
        for _, v in self.data.items():
            self.assertGreaterEqual(len(v), 10,
                                    "Walks line consists of <10 points")
            for coords in v:
                lat = coords[1]
                lon = coords[0]
                self.assertGreaterEqual(lat, 14.3,
                                        "Point in walks out of lat region")
                self.assertLessEqual(lat, 14.6,
                                        "Point in walks out of lat region")
                self.assertGreaterEqual(lon, 47.99,
                                        "Point in walks out of lon region")
                self.assertLessEqual(lon, 48.1,
                                     "Point in walks out of lon region")


if __name__ == '__main__':
    unittest.main()
