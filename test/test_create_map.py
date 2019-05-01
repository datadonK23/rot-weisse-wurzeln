#!/usr/bin/python
""" test_create_map

Author: datadonk23
Date: 30.04.19 
"""

import unittest
from hypothesis import given
import hypothesis.strategies as st

from create_map import map_center, loc, get_info


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
