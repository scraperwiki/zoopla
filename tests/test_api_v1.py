#!/usr/bin/env python
#encoding: utf-8

import unittest
from nose.tools import assert_equal, assert_is_instance, assert_raises

from .context import validate_argument_api_v1 as validate_argument


class TestValidation(unittest.TestCase):
    def test_latitude_is_convertible_to_float(self):
        for lat_long_type in ('latitude', 'longitude', 'lat_min', 'lat_max',
                              'lon_min', 'lon_max'):
            assert_raises(lambda: validate_argument(
                lat_long_type, "(I'm not a valid co-ord)"))

    # TODO: loads more of these!


class TestPropertyListings(unittest.TestCase):
    pass
