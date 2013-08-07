#!/usr/bin/env python
# encoding: utf-8

import requests
import requests_cache
from cStringIO import StringIO

class _ApiVersion1(object):
    def __init__(self, api_key, session_id=None):
        self.api_key = api_key
        print("{}, {}".format(api_key, session_id))

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
        validate_query_arguments(kwargs)
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
    requests_cache.install_cache(
        expire_after=expire_after,
        allowable_methods=('GET',))


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)


def validate_query_arguments(arguments):
    validated = {}
    for argument, value in arguments.items():
        validated[argument] = validate_argument(argument, value)


def validate_argument(name, value):
    try:
        validate_func = globals()['validate_' + name]
    except KeyError:
        return value
    else:
        return validate_func(value)


def validate_area(area):
    return True


def validate_lat_min(value):
    float(value)
    return value
