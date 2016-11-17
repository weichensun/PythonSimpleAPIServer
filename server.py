#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import time
import ssl
import cgi
from _core.router import Router

HOST_NAME = ''
PORT_NUMBER = 5000 # change below 1024 will need sudo permission

# for https
#key_path='_ssl/key.pem'
#cert_path='_ssl/certificate.pem'
key_path = ''
cert_path = ''

class ServerHandler( BaseHTTPRequestHandler ):

    def __init__(self, *args):
        self.router = Router()
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        self.route_process( 'GET' )

    def do_POST(self):
        ctype, pdict = cgi.parse_header( self.headers.getheader( 'content-type' ) )

        post_data = None
        form      = None

        if ctype == 'text/plain':
            post_data = self.rfile.read(int(self.headers.getheader('Content-Length')))
        elif ctype == 'application/x-www-form-urlencoded':
            length = int( self.headers.getheader( 'content-length' ) )
            post_data = cgi.parse_qs( self.rfile.read( length ), keep_blank_values = 1 )
        elif ctype == 'multipart/form-data':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={ 'REQUEST_METHOD':'POST',
                          'CONTENT_TYPE':self.headers['Content-Type']
                }
            )

        self.route_process( 'POST', post_data, form )

    def do_PUT(self):
        self.route_process( 'PUT' )

    def do_DELETE(self):
        self.route_process( 'DELETE' )

    def route_process(self, request_type, post_data = None, form = None ):
        reply = self.router.process( self.path, self.headers, request_type, post_data, form )
        self.do_HEAD( reply.error_code, reply.content_type )
        self.wfile.write( reply.message )
        self.wfile.close()

    def do_HEAD(self, errorCode, content_type):
        self.send_response(errorCode)
        self.send_header('Content-type', content_type)
        self.end_headers()


if __name__ == '__main__':

    server_class = HTTPServer
    httpd = server_class( ( HOST_NAME, PORT_NUMBER ), ServerHandler )
    if key_path != '' and cert_path != '' :
        httpd.socket = ssl.wrap_socket (httpd.socket, keyfile=key_path ,certfile=cert_path, server_side=True)

    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception:
        pass

    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
