#!/usr/bin/env python
# encoding: utf-8

from api_v1 import _ApiVersion1


def api(version, **kwargs):
    if version == 1:
        return _ApiVersion1(**kwargs)
    else:
        raise ValueError("Unsupported API version: '{}'".format(version))
