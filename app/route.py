#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_rules():
    route = {}
    route['default'] = None
    route['/'] = 'app.api.index'
    return route
