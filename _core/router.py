#!/usr/bin/python
# -*- coding: utf-8 -*-

import imp
import sys
import inspect

from _core.base_worker import Base_Worker

def load_worker(module_path, class_name = ''):
    worker = None
    try:
        from_list = module_path.rfind('.')
        module = __import__(module_path)
        module = __import__(module_path, fromlist=[ from_list ] )
        module = imp.reload(module)

        if class_name != '':
            obj = getattr(module, class_name)
            if issubclass(obj, Base_Worker):
                worker = obj
        else:
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name != Base_Worker.__name__ and issubclass(obj, Base_Worker):
                    worker = obj
                    break
        if worker != None:
            worker = worker()

    except:
        print(sys.exc_info()[0])

    return worker


class Reply_Data():
    def __init__(self, message, content_type, error_code):
        self.message        = message
        self.content_type   = content_type
        self.error_code     = error_code


class Router ():

    def process(self, path, headers, request_type, post_data, form):

        url_param_index = path.find('?')
        url_param = ''
        if url_param_index >= 0:
            url_param = path[url_param_index+1:]
            path = path[:url_param_index]

        worker = None
        try:
            route =  __import__('app.route', fromlist = [ 'app' ])
            route = imp.reload( route )
            route_rules = route.get_rules()
            if path in route_rules.keys():
                module_info = route_rules[path]
                if type(module_info) in [list, tuple]:
                    if len(module_info) > 1:
                        worker = load_worker(module_info[0], module_info[1])
                    elif len(module_info) > 0:
                        worker = load_worker(module_info[0])
                elif type(module_info) is str:
                    if '/' in module_info:
                        worker = load_worker(module_info[:module_info.find('/')], module_info[module_info.find('/')+1:])
                    else:
                        worker = load_worker(module_info)

        except ImportError:
            pass

        if worker == None:
            default_404_message = '{"status":404,"message":"NOT_FOUND"}'
            content_type        = 'application/json'
            return Reply_Data(default_404_message, content_type, 404)
        else:
            worker.process(path, headers, url_param, request_type, post_data, form)
            return Reply_Data(worker.message, worker.content_type, worker.error_code)

