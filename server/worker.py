#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import mimetypes
import cgi
import os.path

class Worker():

    def __init__(self, http_handler, route_params, url_query_str):

        # Keep handler to get more data
        self.http_handler = http_handler

        # Request data
        self.request_headers = http_handler.headers
        self.route_params    = route_params
        self.url_query_str   = url_query_str
        self.url_query       = dict()

        # Response data
        self.response_headers = []

    def _send_code_and_header(self, code):
        self.http_handler.send_response(200)

        for headers in self.response_headers:
            self.http_handler.send_header(header[0], header[1])
        self.http_handler.end_headers()

    def _send_message(self, message):
        if message:
            if type(message) is str:
                self.http_handler.wfile.write(message.encode('utf-8'))
            else:
                self.http_handler.wfile.write(message)

    def responseFile(self, file_path, block_size=2048):
        mime_type = mimetypes.guess_type(file_path)[0]
        size      = os.stat(file_path).st_size

        with open(file_path, 'rb') as f:
            self._send_code_and_header(200)
            while True:
                data = f.read(block_size)
                if data:
                    self.http_handler.wfile.write(data)
                else:
                    break
        f.closed


    def responseOK(self, message):
        self._send_code_and_header(200)
        self._send_message(message)

    def responseError(self, error_code, message=''):
        self._send_code_and_header(error_code)
        self._send_message(message)

    def add_response_header(self, header, value):
        self.response_headers.append((header, value))

    def get_request_body(self):
        content_length = int(self.request_headers.get('Content-Length', 0))
        if content_length == 0:
            return None

        content_type = self.request_headers.get('Content-Type', '')
        if content_type == '':
            return None

        ctype, pdict = cgi.parse_header(content_type)

        if ctype == 'multipart/form-data':
            result = None
            form = cgi.FieldStorage(fp=self.http_handler.rfile,
                                    headers=self.http_handler.headers,
                                    environ={
                                        'REQUEST_METHOD':self.http_handler.command,
                                        'CONTENT_TYPE':content_type
                                    })
            # Parse data to dict
            for key in form:
                payload = form[key]
                if type(payload) is list:
                    for item in payload:
                        if result:
                            data = {}
                            data['file_name'] = item.filename
                            data['name'] = item.name
                            data['content'] = item.value
                            result.append(data)
                        else:
                            result= []
                            data = {}
                            data['file_name'] = item.filename
                            data['name'] = item.name
                            data['content'] = item.value
                            result.append(data)
                else:
                    if result:
                        data = {}
                        data['file_name'] = payload.filename
                        data['name'] = payload.name
                        data['content'] = payload.value
                        result.append(data)
                    else:
                        result= []
                        data = {}
                        data['file_name'] = payload.filename
                        data['name'] = payload.name
                        data['content'] = payload.value
                        result.append(data)

            return result

        # application/x-www-form-urlencoded can be complex ...
        # Just return for developer to parse :)
        return self.http_handler.rfile.read(content_length)
