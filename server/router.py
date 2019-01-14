#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import sys
import imp
import re
import inspect

class Route():

    def __init__(self, pattern='/'):
        self.pattern         = pattern
        self.worker          = None
        self.sub_route_nodes = {}
        self.sub_param_nodes = None
        self.is_param_node   = False
        self.param_name      = ''

    def set_param_node(self, param_name):
        self.is_param_node = True
        self.param_name    = param_name

    def add_route(self, route, worker):
        if len(route) == 1:
            self.worker = worker
        else:
            pattern = route[1]
            match = re.search(r"{(\w+)}", pattern)
            if match:
                if self.sub_param_nodes == None:
                    self.sub_param_nodes = Route(pattern)
                self.sub_param_nodes.set_param_node(match.group(1))
                self.sub_param_nodes.add_route(route[1:], worker)
            else:
                sub_node = self.sub_route_nodes.get(pattern, None)
                if not sub_node:
                    sub_node = Route(pattern)
                    self.sub_route_nodes[pattern] = sub_node
                sub_node.add_route(route[1:], worker)

    def get_worker(self, route):
        return self._route_worker(route, {})

    def _route_worker(self, route, route_param):
        # Check is param node
        if self.is_param_node:
            route_param[self.param_name] = route[0]

        # Check current node
        if len(route) == 1:
            if self.pattern == route[0] or self.is_param_node:
                return self.worker, route_param
            else:
                return None, route_param
        else:
            sub_node = self.sub_route_nodes.get(route[1], None)
            if sub_node:
                return sub_node._route_worker(route[1:], route_param)
            elif self.sub_param_nodes:
                return self.sub_param_nodes._route_worker(route[1:], route_param)
            else:
                return None, route_param

    # For test
    def walk(self, level = 0):
        print(self.pattern, "-----", level,"----", self.worker)
        for key in self.sub_route_nodes.keys():
            self.sub_route_nodes[key].walk(level+1)
        if self.sub_param_nodes:
            self.sub_param_nodes.walk()


class Router():

    def __init__(self):
        self._route = Route()

    def _parse_route(self, route):
        if route == '':
            route = '/'
        route = re.split('(/)', route)
        if route[0] == '':
            route.remove('')
        else:
            route.insert(0, '/')
        if route[-1] == '':
            route.remove('')
        return route

    def get_route(self):
        return self._route

    def add_route(self, route, worker):
        self._route.add_route(
            self._parse_route(route),
            worker
        )

    def get_worker(self, route):
        worker = self._route.get_worker(
            self._parse_route(route)
        )
        return worker
