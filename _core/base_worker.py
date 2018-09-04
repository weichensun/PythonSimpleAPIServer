#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from _core import request_types

class Base_Worker():

    def __init__( self ):
        # For reply data
        self.message                = ''
        self.content_type           = ''
        self.code                   = 0

        # Input data (New)
        self.route_parameters       = {}
        self.request_body           = None
        self.request_headers        = None

        # Input data old
        self.headers                = None
        self.url_param              = ''
        self.request_type           = ''
        self.path                   = ''
        self.post_data              = None
        self.form                   = None

    def reply( self, message, content_type, code ):
        self.message = message
        self.content_type = content_type
        self.code = code
        return self.get_response()

    def replyOK(self, message):
        if not self.isstr(message):
            message = self.dict_to_json(message)
        self.message = message + '\n'

        if self.is_json(message):
            self.content_type = "application/json"
        else:
            self.content_type = "text/plain"
        self.code = 200
        return self.get_response()

    def set_request_body(self, request_body):
        self.request_body = request_body

    def set_request_headers(self, request_headers):
        self.request_headers = request_headers

    def set_route_parameters(self, route_parameters):
        self.route_parameters = route_parameters

    def route_parameter(self, key):
        if key in self.route_parameters:
            return self.route_parameters[key]
        return ''

    def get_response(self):
        response = {}
        response['code']            = self.code
        response['content_type']    = self.content_type
        response['message']         = self.message
        return response

    # A tricky way to load methods
    def get_method_list(self):
        return { request_types.GET : self.do_GET,
                 request_types.POST: self.do_POST,
                 request_types.PUT: self.do_PUT,
                 request_types.DELETE: self.do_DELETE }

    def do_GET(self):
        return self.reply('', 'text/plain', 405)

    def do_POST(self):
        return self.reply('', 'text/plain', 405)

    def do_PUT(self):
        return self.reply('', 'text/plain', 405)

    def do_DELETE(self):
        return self.reply('', 'text/plain', 405)

    def isstr(self, input):
        try:
            return isinstance(input, basestring) # For python2
        except NameError:
            return isinstance(input, str) # For python 3

    def is_json(self, input):
        if not self.isstr(input):
            return False
        try:
            json.loads(input)
        except ValueError:
            return False
        return True

    def dict_to_json(self, input):
        try:
            return json.dumps(input)
        except:
            Log.le("Cannot parse to JSON")
            return str(input)
