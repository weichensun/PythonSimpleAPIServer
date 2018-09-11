#!/usr/bin/python
# -*- coding: utf-8 -*-

class HttpResponse:

    def __init__(self, error_code, headers=[], data=''):
        self.error_code = error_code
        self.headers  = headers
        self.data = data

    def get_data(self):
        return self.data

    def get_headers(self):
        return self.headers

    def get_error_code(self):
        return self.error_code
