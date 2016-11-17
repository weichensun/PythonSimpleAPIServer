#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.router import load_worker

def get_worker( path ):
    if path == '/':
        return load_worker( 'route.index' )
    return None
