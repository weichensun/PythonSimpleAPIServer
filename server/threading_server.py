#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[0] < 3:
#    from BaseHTTPServer import HTTPServer
    import SocketServer
else:
#    from http.server import HTTPServer
    import socketserver as SocketServer

from .http_server import HTTPServer

class ThreadingHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):
    daemon_threads = True
