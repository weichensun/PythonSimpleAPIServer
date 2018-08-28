#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core import request_types

class Processor():

    def process(self, request_type, worker):

        response = {}
        try:
            # Use method list to avoid if ... elif ...
            response = worker.get_method_list()[request_type]()

            if response == None:
                response = {}
                response['code'] = 200
                response['content_type'] = "text/plain"
                response['message'] = ''

        except KeyError:
            response = {}
            response['code'] = 405
            response['content_type'] = "text/plain"
            response['message'] = ''
        except:
            response = {}
            response['code'] = 500
            response['content_type'] = "aplication/json"
            response['message'] = '{"message": "INTERNAL_SERVER_ERROR"}'
            pass

        return response
