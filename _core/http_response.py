#!/usr/bin/python
# -*- coding: utf-8 -*-

class HttpResponse:

    def __init__(self, error_code, headers=[], data=''):
        self.error_code = error_code
        self.headers  = headers
        self.data = data

    def addHeader(self, key, value):
        self.header.append((key, value))

    def setHeader(self, headers):
        self.headers = headers

    def setData(self, data):
        self.data = data

    def sefErrorCode(self, error_code):
        self.error_code = error_code

    def getData(self):
        return self.data

    def getHeaders(self):
        return self.headers

    def getErrorCode(self):
        return self.error_code
