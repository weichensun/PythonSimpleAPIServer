#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] < 3:
    from BaseHTTPServer import HTTPServer as PyHTTPServer
else:
    from http.server import HTTPServer as PyHTTPServer


class HTTPServer(PyHTTPServer):

    def __init__(self, server_address, RequestHandlerClass, router, auth_function=None, debug=False):
        PyHTTPServer.__init__(self, server_address, RequestHandlerClass)
        self._router        = router
        self.auth_function  = auth_function
        self.debug          = debug

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        # Pass route to handler class
        self.RequestHandlerClass(request, client_address, self, self._router, self.auth_function, self.debug)

