#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import mimetypes
import os.path
import _core.exceptions as Execptions
from _core.http_response import HttpResponse

class BaseWorker():

    def __init__(self, route_parameters, request_headers):

        # Hander
        # We store handler here, so we can ask handler for more data
        self.request_hander         = request_headers

        # Input data (New)
        self.route_parameters       = route_parameters
        self.request_headers        = request_headers.headers
        self.request_body           = ''

        # Output data
        self.response_headers       = []

        if not self.check_authorization():
            raise Execptions.Unauthorized


    #
    # Functions for retrive data
    #
    def get_route_parameter(self, key, default=None):
        if key in self.route_parameters:
            return self.route_parameters[key]
        return default

    def get_request_header(self, key, default=None):
        header = self.request_headers.get(key)
        if header != None:
            return header
        return default

    #
    # Functions for response
    #
    def reply(self, error_code, message):
        return HttpResponse(error_code, headers=self.response_headers, data=message)

    def replyFile(self, file_path):
        if os.path.exists(file_path):
            try:
                data = ''
                with open(file_path, 'rb') as file:
                    data = file.read()
                    mime_type = mimetypes.guess_type(file_path)[0]
                    self.add_response_header('content-length', str(len(data)))
                    self.add_response_header('content-type', str(mime_type))
                    return HttpResponse(200, headers=self.response_headers, data=data)
            except:
                raise Execptions.Forbidden
        raise Execptions.NotFound

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

        self.add_response_header('content-length', str(len(message)))
        self.add_response_header('content-type', content_type)
        return HttpResponse(200, headers=self.response_headers, data=message)

    def add_response_header(self, header, value):
        self.response_headers.append((header, value))

    def check_authorization(self):
        return True
