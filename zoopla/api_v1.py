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


class PropertyListing(object):
    def __init__(self, member_variables):
        self.__dict__ = member_variables


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

    def _call_api(self, command, arguments):
        validate_query_arguments(arguments)
        url = self._make_url('property_listings', arguments)
        f = download_url(url)
        return json.loads(f.read())

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

    def _call_api_paged(self, command, args, max_results, result_processor):
        """
        There are a few conditions where we need to stop paging
        1) We've yielded max_results
        2) We've yielded result_count
        """
        num_yielded = 0
        args['page_size'] = 100
        args['page_number'] = 1
        result_count = None

        def reached_limit(number, limit):
            return number >= limit if limit is not None else False

        def finished():
            L.debug("yielded: {}, max_results: {}, result_count: {}".format(
                num_yielded, max_results, result_count))
            if reached_limit(num_yielded, max_results):
                L.debug("Stop paging, yielded={}, max_results={}".format(
                    num_yielded, max_results))
                return True
            elif reached_limit(num_yielded, result_count):
                L.debug("Stop paging, yielded={}, result_count={}".format(
                    num_yielded, result_count))
                return True
            else:
                return False

        while not finished():
            response = self._call_api('property_listings', args)
            result_count = response['result_count']

            for listing in result_processor(response):
                yield listing
                num_yielded += 1
                if finished():
                    break
            args['page_number'] += 1

    def property_listings(self, max_results=100, **kwargs):
        L.debug('property_listings(max_results={}, {})'.format(
            max_results, kwargs))
        result_processor = self._create_listings
        if 'page_size' not in kwargs and 'page_number' not in kwargs:
            L.debug("Automatically paging this request.")
            generator = self._call_api_paged(
                'property_listings',
                kwargs,
                max_results,
                result_processor)

        else:
            L.debug("Not paging this request.")
            generator = self.create_listings(
                self._call_api('property_listings', kwargs))

        for listing in generator:
            yield listing

    def _create_listings(self, api_response):
        response_meta = dict(api_response)
        del response_meta['listing']
        L.debug("response meta: {}".format(response_meta))

        listings = api_response['listing']
        L.debug("{} listings".format(len(listings)))

        for listing in listings:
            listing['meta'] = response_meta
            yield PropertyListing(listing)

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
