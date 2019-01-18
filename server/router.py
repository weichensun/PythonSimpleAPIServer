#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class Router():

    def __init__(self):
        self._route = {
            '/': {
                'sub_nodes': {},
                'param_node': None,
                'worker': None
            }
        }

    def get_route(self):
        return self._route

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


    def add_worker(self, route, worker):
        nodes = self._parse_route(route)
        node_lists = self._route
        parent_node = self._route

        for node in nodes:
            match = re.search(r"{(\w+)}", node)
            if match:
                if parent_node['param_node'] == None:
                    parent_node['param_node'] = {
                        'sub_nodes': {},
                        'param_node': None,
                        'pattern': None,
                        'worker': None
                    }
                parent_node['param_node']['pattern'] = match.group(1)
                parent_node = parent_node['param_node']
                node_lists = parent_node['sub_nodes']
            else:
                if node not in node_lists:
                    node_lists[node] = {
                        'sub_nodes': {},
                        'param_node': None,
                        'worker': None
                    }
                parent_node = node_lists[node]
                node_lists  = node_lists[node]['sub_nodes']

        parent_node['worker'] = worker


    def get_worker(self, route):
        nodes       = self._parse_route(route)
        node_lists  = self._route
        parent_node = self._route
        route_params = {}

        for node in nodes:
            if node in node_lists:
                parent_node = node_lists[node]
                node_lists = node_lists[node]['sub_nodes']
            else:
                if parent_node['param_node']:
                    route_params[parent_node['param_node']['pattern']] = node
                    parent_node = parent_node['param_node']
                    node_lists = parent_node['sub_nodes']
                else:
                    return None, route_params

        return parent_node['worker'], route_params

