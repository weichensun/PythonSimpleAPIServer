#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from _core.http_response import HttpResponse

class BaseWorker():

    def __init__(self):
        # For reply data
        self.message                = ''
        self.content_type           = ''
        self.code                   = 0

        # Hander
        # Ask handler for data
        self.request_hander         = None

        # Input data (New)
        self.route_parameters       = {}
        self.request_body           = None
        self.request_headers        = None

        # Input data old
#        self.headers                = None
#        self.url_param              = ''
#        self.request_type           = ''
#        self.path                   = ''
#        self.post_data              = None
#        self.form                   = None

    def set_request_handler(self, handler):
        self.request_handler = handler

    def replyOK(self, message):
        content_type = 'text/plain; charset=utf-8'
        if type(message) in [dict, list]:
            message = json.dumps(message)
            content_type = 'application/json'
        else:
            try:
                json.loads(message)
                content_type = 'application/json'
            except ValueError:
                pass

        return HttpResponse(200, headers=[], data=message)

    def set_request_body(self, request_body):
        self.request_body = request_body

    def set_request_headers(self, request_headers):
        self.request_headers = request_headers

    def set_route_parameters(self, route_parameters):
        self.route_parameters = route_parameters

    def get_route_parameter(self, key, default=''):
        if key in self.route_parameters:
            return self.route_parameters[key]
        return default

