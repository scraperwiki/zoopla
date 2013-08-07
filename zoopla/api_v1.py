#!/usr/bin/env python
# encoding: utf-8

import requests
import requests_cache
from cStringIO import StringIO
import json
from urllib import urlencode
import logging
L = logging.getLogger(__name__)

BASE_URL = 'http://api.zoopla.co.uk/api/v1/'


class _ApiVersion1(object):
    def __init__(self, api_key, session_id=None, cache_seconds=(12 * 60 * 60)):
        self.api_key = self._validate_api_key(api_key)
        if cache_seconds:
            install_cache(cache_seconds)

    def _validate_api_key(self, api_key):
        if len(api_key) < 24:
            raise ValueError("Invalid API key(?): '{}'".format(api_key))
        return api_key

    def _make_url(self, command, arguments):
        arguments['api_key'] = self.api_key
        url = "{}{}.js?{}".format(BASE_URL, command,
                                  urlencode(sort_dict(arguments)))
        L.debug(url)
        return url

    def zed_index(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def area_value_graphs(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def property_rich_list(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def average_area_sold_price(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def area_zed_indices(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def zoopla_estimates(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def average_sold_prices(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def property_listings(self, **kwargs):
        L.info('property_listings: {}'.format(kwargs))
        validate_query_arguments(kwargs)
        url = self._make_url('property_listings', kwargs)
        f = download_url(url)
        result = json.loads(f.read())
        L.debug(result)
        raise NotImplementedError("This method isn't yet implemented.")

    def get_session_id(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def refine_estimate(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def arrange_viewing(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def local_info_graphs(self):
        raise NotImplementedError("This method isn't yet implemented.")

    def property_historic_listings(self):
        raise NotImplementedError("This method isn't yet implemented.")


def install_cache(expire_after):
    L.info("Installing cache, valid for {} seconds.".format(expire_after))
    requests_cache.install_cache(
        expire_after=expire_after,
        allowable_methods=('GET',))


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)


def sort_dict(some_dict):
    """

    Return a unicode:unicode dictionary, sorted by the key.
    >>> sort_dict({'b': 1, 'a': 2})
    [('a', 2), ('b', 1)]
    """
    return sorted(some_dict.items())


def validate_query_arguments(arguments):
    validated = {}
    for argument, value in arguments.items():
        validated[argument] = validate_argument(argument, value)


def validate_argument(name, value):
    validate_func_name = 'validate_' + name
    try:
        validate_func = globals()[validate_func_name]
    except KeyError:
        L.debug("No function {}(..), returning '{}' as '{}'".format(
            validate_func_name, name, value))
        return value
    else:
        L.debug("Calling {}({})".format(validate_func_name, value))
        return validate_func(value)


def validate_area(area):
    return True


def validate_lat_min(value):
    float(value)
    return value
