#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

# Custom Handler
from .threading_server import ThreadingHTTPServer
from .http_server import HTTPServer
from .http_handler import HTTPHandler
from .router import Router

class Server:

    def __init__(self):
        self._cert_file_path = None
        self._key_file_path  = None
        self._http_handler   = HTTPHandler
        self._server         = None
        self._router         = Router()

    def set_ssl_cert(self, cert_file_path, key_file_path):
        self._cert_file_path = cert_file_path
        self._key_file_path  = key_file_path

    def add_worker(self, request_path, worker_class):
        self._router.add_worker(request_path, worker_class)

    def run(self, host='0.0.0.0', port='auto', debug=False, threading=False):

        ssl_enabled = False
        if port == 'auto':
            if self._cert_file_path != None and self._key_file_path != None :
                port = 443
                ssl_enabled = True
            else:
                port = 80

        if threading:
            self._server = ThreadingHTTPServer((host, port), HTTPHandler, self._router, debug)
        else:
            self._server = HTTPServer((host, port), HTTPHandler, self._router, debug)

        self._server.allow_reuse_address = True

        try:
            self._server.serve_forever()
        except(KeyboardInterrupt, SystemExit):
            pass
        except(Exception):
            pass
        finally:
            self._server.server_close()
            sys.exit()
            exit(0)
