#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core import request_types

class Processor():

    def process(self, request_type, worker):

        response = {}
        try:
            # Use method list to avoid if ... elif ...
            worker.get_method_list()[request_type]()
            response = worker.get_response()

        except KeyError:
            response['code'] = 405
            response['content_type'] = "text/plain"
            response['message'] = ''
        except:
            response['code'] = 500
            response['content_type'] = "aplication/json"
            response['message'] = '{"message": "INTERNAL_SERVER_ERROR"}'
            pass

        return response
