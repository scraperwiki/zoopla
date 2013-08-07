#!/usr/bin/env python
# encoding: utf-8

class _ApiVersion1(object):
    def __init__(self, api_key, session_id=None):
        self.api_key = api_key
        print("{}, {}".format(api_key, session_id))

