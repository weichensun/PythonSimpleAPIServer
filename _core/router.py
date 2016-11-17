#!/usr/bin/python
# -*- coding: utf-8 -*-

import imp

def load_worker( path ):

    from_list = path[:path.rfind('.')]
    try:
        module = __import__( path, fromlist=[ from_list ] )
        module = imp.reload(module)
    except ImportError:
        return None

    if hasattr(module, 'API_Worker'):
        return module.API_Worker()

    return None


class Reply_Data():
    def __init__(self, message, content_type, error_code):
        self.message        = message
        self.content_type   = content_type
        self.error_code     = error_code


class Router ():

    def process( self, path, headers, request_type, post_data, form ):

        url_param_index = path.find('?')
        url_param = ''
        if url_param_index >= 0:
            url_param = path[url_param_index+1:]
            path = path[:url_param_index]

        worker = None
        try:
            route_rule = __import__( 'route._route_rules', fromlist = [ 'route' ] )
            route_rule = imp.reload( route_rule )
            worker = route_rule.get_worker( path )
        except ImportError:
            pass

        if worker == None:
            default_404_message = '{"status":404,"message":"NOT_FOUND"}'
            content_type        = 'application/json'
            return Reply_Data( default_404_message, content_type, 404 )
        else:
            worker.process( path, headers, url_param, request_type, post_data, form )
            return Reply_Data( worker.message, worker.content_type, worker.error_code )
