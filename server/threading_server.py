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

#import threading
#import socket
#import errno

class ThreadingHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):
    daemon_threads = True

#class ThreadingHTTPServer(HTTPServer):

#    def process_request(self, request, client_address):
#        thread = threading.Thread(target=self.__new_request, args=(self.RequestHandlerClass, request, client_address))
#        thread.start()

#    def __new_request(self, handlerClass, request, address):
#        try:
#            handlerClass(request, address, self)
#        except socket.error as e:
#            if e.errno != errno.EPIPE:
#                raise
#            pass
#        finally:
#            self.shutdown_request(request)

