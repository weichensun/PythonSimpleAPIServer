#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] < 3:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from urlparse import urlparse
else:
    from http.server import BaseHTTPRequestHandler
    from urllib.parse import urlparse

import json
import time
from _core import request_types
from _core.router import Router
from _core.processor import Processor
from _core.log import Log

class Http_Handler(BaseHTTPRequestHandler):

    def __init__(self, *args):
        self.router     = Router()
        self.processor  = Processor()
        self.duration   = 0
#       For modify response header like Server: SimpleHTTP/0.6 Python/2.7.3
#        self.server_version = ''
#        self.sys_version = ''
        BaseHTTPRequestHandler.__init__(self, *args)

    def log_message(self, format, *args):
        client_addr = self.headers.get('X-Forwarded-For')
        if client_addr == None:
            client_addr = self.client_address[0]
        code = args[1]
        request_info = args[0].split()
        request_type = request_info[0]
        request_path  = request_info[1]
        Log.l("[REQUEST][%s][%s][%s][%s][%s][%.2f ms]" % (time.asctime(), client_addr, code, request_type, request_path, self.duration))

    def do_GET(self):
        self.process(request_types.GET)

    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        request_body = {}
        request_body['type'] = self.headers.get('content-type')
        request_body['data'] = self.rfile.read(content_len)
        self.process(request_types.POST, request_body)

    def do_PUT(self):
        self.process(request_types.PUT)

    def do_DELETE(self):
        self.process(request_types.DELETE)

    def process(self, request_type, request_body = None):
        begin_time = time.time()
        # process url
        parsed_url      = urlparse(self.path)
        resource_path   = parsed_url.path
        url_query       = parsed_url.query

        # get worker
        worker = self.router.get_worker_by_path(resource_path)
        if worker == None:
            self.write_header(404, 'application/json')
            self.write_response('{"status":404,"message":"NOT_FOUND"}')
        else:
            # Start worker
            worker.set_request_body(request_body)
            worker.set_request_headers(None)
            response = self.processor.process(request_type, worker)
            self.duration = (time.time() - begin_time) * 1000
            self.write_header(response['code'], response['content_type'])
            self.write_response(response['message'])

        # close wfile for python2.x
        if sys.version_info[0] < 3:
            self.wfile.close()

    def get_input_data(self, request_type):
        return None

    def write_header(self, errorCode, content_type):
        self.send_response(errorCode)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def write_response(self, message):
        if type(message) is str:
            self.wfile.write(str.encode(message))
        else:
            self.wfile.write(message)
