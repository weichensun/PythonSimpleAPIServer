#!/usr/bin/python
# -*- coding: utf-8 -*-

class API_Worker_Base():

    def __init__( self ):
        self.message                = ''
        self.content_type           = ''
        self.error_code             = 0
        self.headers                = None
        self.url_param              = ''
        self.request_type           = ''
        self.path                   = ''
        self.post_data              = None
        self.form                   = None

    def reply( self, message, content_type, error_code ):
        self.message = message
        self.content_type = content_type
        self.error_code = error_code

    def process( self, path, headers, url_param, request_type, post_data, form ):

        self.path           = path
        self.headers        = headers
        self.url_param      = url_param
        self.request_type   = request_type
        self.post_data      = post_data
        self.form           = form

        if request_type == 'GET':
            self.do_GET()
        elif request_type == 'POST':
            self.do_POST()
        elif request_type == 'PUT':
            self.do_PUT()
        elif request_type == 'DELETE':
            self.do_DELETE()
        else:
            self.reply( '', 'text/html', 405 )

    def do_GET( self ):
        self.reply( '', 'text/html', 405 )

    def do_POST( self ):
        self.reply( '', 'text/html', 405 )

    def do_PUT( self ):
        self.reply( '', 'text/html', 405 )

    def do_DELETE( self ):
        self.reply( '', 'text/html', 405 )









