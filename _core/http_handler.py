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
import traceback
from _core.http_router import HttpRouter
from _core.log import Log
import _core.exceptions as Execptions

class Http_Handler(BaseHTTPRequestHandler):

    def __init__(self, *args):
        self.duration   = 0
        # For modify response header like Server: SimpleHTTP/0.6 Python/2.7.3
        # self.server_version = ''
        # self.sys_version = ''
        BaseHTTPRequestHandler.__init__(self, *args)

    def get_worker(self, path):
        return HttpRouter.get_worker_by_path(urlparse(self.path).path, self)

    def write_response(self, response):

        self.send_response(response.get_error_code())
        for header in response.get_headers():
            self.send_header(header[0], header[1])
        self.end_headers()
        data = response.get_data()

        if type(data) is str and sys.version_info[0] >= 3:
            self.wfile.write(str.encode(data))
        else:
            # For python 2 and python 3 byte data
            self.wfile.write(data)

        # Close for python version < 3
        if sys.version_info[0] < 3:
            self.wfile.close()


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

            ### Custom add route to get worker
            try:
                worker = self.get_worker(self.path)
                if worker == None:
                   self.send_error(404, "Not found (%s)" % self.path)
                   return
            except Execptions.Unauthorized:
                self.send_error(401, "Unauthorized")
                return

            # Check worker has method attr
            mname = 'do_' + self.command
            if not hasattr(worker, mname):
                self.send_error(501, "Unsupported method (%r)" % self.command)
                return
            try:
                method = getattr(worker, mname)
                http_response = method()
                self.write_response(http_response)
            except Execptions.Forbidden:
                self.send_error(403, "Forbidden")
            except Execptions.NotFound:
                self.send_error(404, "Not found (%s)" % self.path)
            except Execptions.BadRequest:
                self.send_error(400, "Bad Request")
            except Exception as e:
                err_log = str(e) + "\n\n" + traceback.format_exc()
                Log.l(err_log)
                self.send_error(500, "Something went wrong (-)")
            finally:
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
