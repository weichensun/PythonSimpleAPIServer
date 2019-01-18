#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

if sys.version_info[0] >= 3:
    # Import Python3
    from http.server import BaseHTTPRequestHandler
    import urllib.parse as urlparse

else:
    # Import Python2.7
    from BaseHTTPServer import BaseHTTPRequestHandler
    import urlparse

import json
import time
import socket
import traceback

# Extend and overwrite BaseHTTPRequestHandler
# Since this file is direct extends from BaseHTTPRequestHandler, follows BaseHTTPRequestHandler's coding style
class HTTPHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server, router, debug, auth=None):

        # For modify response header "Server: SimpleHTTP/0.6 Python/2.7.3"
        # self.server_version = ''
        # self.sys_version = ''

        self.debug  = debug
        self.router = router
        self.auth   = auth

        self.response_headers = {}      # Use dict to avoid duplicate headers
        self.headers_send     = False


        # the actual process
        # Declare variables before this function, or above ...
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)


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
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return

            # Global AUTH check
            #
            #   ....
            #

            if self.auth:
                if not self.auth():
                    self.send_error(404, "Unauthorized")
                    return

            url_result = urlparse.urlsplit(self.path)
            worker_class, route_params = self.router.get_worker(url_result.path)

            if not worker_class:
                self.send_error(404, "Not found (%s)" % self.path)
                return

            worker = worker_class(self, route_params, url_result.query)

            # Process HTTP Method
            mname = 'do_' + self.command
            if not hasattr(worker, mname):
                self.send_error(501, "Unsupported method (%r)" % self.command)
                return


            method = getattr(worker, mname)
            method()

        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
        except Exception as e:

            trace = None
            if self.debug:
                trace = traceback.format_exc()

            # Check 403
            if 'Permission denied' in e.args:
                # Python3 = 'PermissionError'
                # Python2 = 'OSError'
                self.send_error(403, "Forbidden", trace)

            # Check 404
            elif 'No such file or directory' in e.args:
                # Python3 = 'FileNotFoundError'
                # Python2 = 'OSError'
                self.send_error(404, "Not found", trace)

            else:
            # Other errors
                self.send_error(500, "Internal Server Error", trace)
#            self.close_connection = True

        finally:
            if not self.wfile.closed:
                self.wfile.flush() #actually send the response if not already done.


    def format_message(self, code, message=None, debug_message=None, data=None):
        output = {
            'status'  : code,
            'message' : message,
            'data'    : data,
        }

        if self.debug:
            output['_debug'] = debug_message

        return json.dumps(output)


    def send_error(self, code, message=None, debug_message=None):
        self.response_headers['Connection'] = 'close'
        self.send_message(code, message, debug_message)


    def send_message(self, code, message=None, debug_message=None):
        self.send_headers(code)
        if self.command != 'HEAD' and message:
            self.wfile.write(self.format_message(code, message, debug_message).encode('utf-8'))

    def send_data(self, data):
        # Make sure 'send_headers' is called once before use this function
        if self.command != 'HEAD' and data:
            self.wfile.write(data)

    def send_headers(self, code):
        if not self.headers_send:
            self.send_response(code)
            for header, value in self.response_headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.headers_send = True

    def send_debug_message(self, message):
        if not self.headers_send:
            self.send_headers(200)
            self.headers_send = True
        self.wfile.write(message.encode('utf-8'))

    def log_message(self, format, *args):
        return
