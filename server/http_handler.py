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
import urlparse

# Extend and overwrite BaseHTTPRequestHandler
class HTTPHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server, router, debug):

        # For modify response header "Server: SimpleHTTP/0.6 Python/2.7.3"
        # self.server_version = ''
        # self.sys_version = ''
        self.debug  = debug
        self.router = router

        # the actual process
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

            #(worker, middleware_class, params)
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

#            self.wfile.flush() #actually send the response if not already done.
        except socket.timeout as e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
        except PermissionError as e:
            self.send_error(403, "403 Forbidden (%s)\n\n%s\n%s" % (self.path, str(e), traceback.format_exc()))
            self.close_connection = True
        except FileNotFoundError as e:
            self.send_error(404, "404 Not found (%s)\n\n%s\n%s" % (self.path, str(e), traceback.format_exc()))
            self.close_connection = True
        except Exception as e:
            self.send_error(500, "500 Internal Server Error (%s)\n\n%s\n%s" % (self.path, str(e), traceback.format_exc()))
            self.close_connection = True
        finally:
            self.wfile.flush() #actually send the response if not already done.


    def send_error(self, code, message=None):

        self.send_response(code)
        self.end_headers()

        if self.debug and self.command != 'HEAD' and message:
            if type(message) is str:
                self.wfile.write(message.encode('utf-8'))
            else:
                self.wfile.write(message)

