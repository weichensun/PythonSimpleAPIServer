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
import socket
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

    def do_GET(self):
        self.process(request_types.GET)

    # [This need to fix]
    # Since we add this method
    # For 501 cases client need to POST the entire data to know the server does not have that method
    # And server recesive data that does not needed ...
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

    ### Override BaseHTTPRequestHandler ###
    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return

            worker = self
            # Route self.path, find worker
            # TO-DO

            # if worker = None:
            #   self.send_error(404, "Not found (%s)" % self.path)
            #   return

            # Check worker has method attr
            mname = 'do_' + self.command
            if not hasattr(worker, mname):
                self.send_error(501, "Unsupported method (%r)" % self.command)
                return
            method = getattr(worker, mname)
            method()
            self.wfile.flush() #actually send the response if not already done.
        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return

    def log_request(self, code='-', size='-'):
        client_addr = self.headers.get('X-Forwarded-For')
        if client_addr == None:
            client_addr = self.client_address[0]
        Log.l("[RESPONSE][%s][%s][%s][%s][%s][%.2fms]" % (time.asctime(),
                                                         client_addr,
                                                         self.command,
                                                         self.path,
                                                         code,
                                                         self.duration))

    def log_error(self, format, *args):
        client_addr = self.headers.get('X-Forwarded-For')
        if client_addr == None:
            client_addr = self.client_address[0]
        Log.l("[ERROR][%s][%s][%s][%s][%s]" % (time.asctime(),
                                           client_addr,
                                           self.command,
                                           self.path,
                                           format%args))
