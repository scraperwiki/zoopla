#!/usr/bin/env python
#encoding: utf-8

import unittest
from nose.tools import assert_equal, assert_is_instance, assert_raises

from .context import zoopla
from .context import _ApiVersion1


class TestApiFactory(unittest.TestCase):
    def test_no_arguments_is_failure(self):
        assert_raises(TypeError, lambda: zoopla.api())

    def test_no_api_key_is_failure(self):
        assert_raises(TypeError, lambda: zoopla.api(version=1))

    def test_no_version_is_failure(self):
        assert_raises(TypeError, lambda: zoopla.api(api_key='foo'))

    def test_version_1_returns_correct_class(self):
        api = zoopla.api(version=1, api_key='some_api_key')
        assert_is_instance(api, _ApiVersion1)
        assert_equal('some_api_key', api.api_key)
