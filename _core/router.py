#!/usr/bin/python
# -*- coding: utf-8 -*-

import imp
from _core.base_worker import Base_Worker
from _core.worker_loader import Worker_Loader

class Router ():

    def __init__(self):
        self.worker_loader = Worker_Loader()

    def get_worker(self, path):
        worker = None
        try:
            route =  __import__('app.route', fromlist = [ 'app' ])
            route = imp.reload( route )
            route_rules = route.get_rules()
            if path in route_rules.keys():
                module_info = route_rules[path]
                if type(module_info) in [list, tuple]:
                    if len(module_info) > 1:
                        worker =  self.worker_loader.load(module_info[0], module_info[1])
                    elif len(module_info) > 0:
                        worker =  self.worker_loader.load(module_info[0])
                elif type(module_info) is str:
                    if '/' in module_info:
                        worker =  self.worker_loader.load(module_info[:module_info.find('/')], module_info[module_info.find('/')+1:])
                    else:
                        worker =  self.worker_loader.load(module_info)

        except ImportError:
            pass

        return worker

