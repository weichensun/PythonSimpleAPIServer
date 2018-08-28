#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

if sys.version_info[0] < 3:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
else:
    from http.server import BaseHTTPRequestHandler, HTTPServer

import threading
import resource
import json
import time
import ssl
import cgi
from _core.router import Router
from _core.http_handler import Http_Handler

# Settings
#
HOST_NAME = '0.0.0.0'
PORT_NUMBER = 5000 # change below 1024 will need sudo permission

# For https configuration
# SSL_CERTIFICATE_FILE='{PATH}/key.pem'
# SSL_CERTIFICATE_KEY_FILE='{PATH}/certificate.pem'
#
SSL_CERTIFICATE_PUBLIC_KEY_FILE = ''
SSL_CERTIFICATE_PRIVATE_KEY_FILE = ''

# Reference from
# https://stackoverflow.com/questions/19537132
#
class ThreadedHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        thread = threading.Thread(target=self.__new_request, args=(self.RequestHandlerClass, request, client_address, self))
        thread.start()
    def __new_request(self, handlerClass, request, address, server):
        handlerClass(request, address, server)
        self.shutdown_request(request)

# Main
#
if __name__ == '__main__':

    server_class = ThreadedHTTPServer
#    httpd = server_class((HOST_NAME, PORT_NUMBER), ServerHandler)
    httpd = server_class((HOST_NAME, PORT_NUMBER), Http_Handler)
    if SSL_CERTIFICATE_PUBLIC_KEY_FILE != '' and SSL_CERTIFICATE_PRIVATE_KEY_FILE != '' :
        httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=SSL_CERTIFICATE_PUBLIC_KEY_FILE,
                                        certfile=SSL_CERTIFICATE_PRIVATE_KEY_FILE, server_side=True)

    print("%s Server Starts - %s:%s" % (time.asctime(), HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception:
        pass

    httpd.server_close()
    print("%s Server Stops - %s:%s" % (time.asctime(), HOST_NAME, PORT_NUMBER))


