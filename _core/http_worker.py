#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import mimetypes
import cgi
import os.path
import _core.exceptions as Execptions
from _core.http_response import HttpResponse

class HttpWorker():

    def __init__(self, route_parameters, request_handler):

        # Hander
        # We store handler here, so we can ask handler for more data
        self.request_handler         = request_handler

        # Input data (New)
        self.route_parameters       = route_parameters
        self.request_headers        = request_handler.headers
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

    def get_request_headers(self):
        return self.request_headers

    def get_request_header(self, key, default=None):
        header = self.request_headers.get(key)
        if header != None:
            return header
        return default

    def get_post_data(self):
        content_length = int(self.get_request_header('Content-Length', 0))
        if content_length == 0:
            return ''

        content_type = self.get_request_header('Content-Type', '')
        if content_type == '':
            return ''

        ctype, pdict = cgi.parse_header(content_type)

        if ctype == 'multipart/form-data':
#            fields = cgi.parse_multipart(self.request_handler.rfile, pdict)
#            print fields
#            messagecontent = fields.get('upload_file')
            return ''

#        if ctype == 'application/x-www-form-urlencoded':
#            return ''

        return self.request_handler.rfile.read(content_length)


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
