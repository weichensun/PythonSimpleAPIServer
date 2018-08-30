#!/usr/bin/python
# -*- coding: utf-8 -*-

class BaseRoute():

    class Route():
        def __init__(self, pattern, worker_module_path):
            self.pattern = pattern
            self.worker_module_path = worker_module_path

    def __init__(self):
        self.route_list = []
        self.set_route()

    def add(self, pattern, worker_module_path):
        self.route_list.append(BaseRoute.Route(pattern, worker_module_path))

    def set_route(self):
        pass
