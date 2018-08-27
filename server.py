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


# Custom Handler
#
class ServerHandler(BaseHTTPRequestHandler):

    def __init__(self, *args):
        self.router = Router()
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        self.route_process('GET')

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        post_data = None
        form      = None

        if ctype == 'text/plain':
            post_data = self.rfile.read(int(self.headers.getheader('Content-Length')))
        elif ctype == 'application/json':
            post_data = json.loads(self.rfile.read(int(self.headers.getheader('Content-Length'))))
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            post_data = cgi.parse_qs(self.rfile.read(length), keep_blank_values = 1)
        elif ctype == 'multipart/form-data':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={ 'REQUEST_METHOD':'POST',
                          'CONTENT_TYPE':self.headers['Content-Type']
                }
            )

        self.route_process('POST', post_data, form)

    def do_PUT(self):
        self.route_process('PUT')

    def do_DELETE(self):
        self.route_process('DELETE')

    def route_process(self, request_type, post_data = None, form = None):
        reply = self.router.process(self.path, self.headers, request_type, post_data, form)
        self.do_HEAD(reply.error_code, reply.content_type)
        if sys.version_info[0] < 3:
            self.wfile.write(reply.message)
            self.wfile.close()
        else:
            self.wfile.write(str.encode(reply.message))
            # It seem like python 3 will close/flush automatically

    def do_HEAD(self, errorCode, content_type):
        self.send_response(errorCode)
        self.send_header('Content-type', content_type)
        self.end_headers()

# Main
#
if __name__ == '__main__':

    server_class = ThreadedHTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ServerHandler)

    if SSL_CERTIFICATE_PUBLIC_KEY_FILE != '' and SSL_CERTIFICATE_PRIVATE_KEY_FILE != '' :
        httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=SSL_CERTIFICATE_PUBLIC_KEY_FILE, certfile=SSL_CERTIFICATE_PRIVATE_KEY_FILE, server_side=True)

    print("%s Server Starts - %s:%s" % (time.asctime(), HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception:
        pass

    httpd.server_close()
    print("%s Server Stops - %s:%s" % (time.asctime(), HOST_NAME, PORT_NUMBER))


