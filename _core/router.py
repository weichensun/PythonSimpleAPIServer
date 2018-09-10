#!/usr/bin/python
# -*- coding: utf-8 -*-

import imp
import re
from _core.worker_loader import Worker_Loader

class Router ():


    class Match():
        def __init__(self, route_parameters):
            self.route_parameters = route_parameters

#    def __init__(self):
#        self.worker_loader = Worker_Loader()

    @classmethod
    def get_worker_by_path(self, path):
        worker = None
        try:
            route = __import__('app.route', fromlist = ['app'])
            route = imp.reload(route)
            route = route.Route()

            for route in route.route_list:
                matched = self.match_pattern_and_path(route.pattern, path)
                if matched:
                    worker = Worker_Loader.load(route.worker_module_path)
                    worker.set_route_parameters(matched.route_parameters)
                    break

        except ImportError:
            pass

        return worker

    @classmethod
    def match_pattern_and_path(self, rule, path):
        key_pattern = "{(\w*)}|{(\w*)\|[n,c]}"
        match_list = re.findall(key_pattern, rule)

        key_list = []
        for idx, match in enumerate(match_list):
            if match[0] != '':
                key_list.append(match[0])
            elif match[1] != '':
                key_list.append(match[1])
            else:
                key_list.append("VAR_" + str(idx))

        if len(key_list) > 0:
            rule = re.sub("{\w*}", "([\'\.\*\w+!(),\-\$\%]+)", rule)
            rule = re.sub("{\w*\|n}", "(\d+)", rule)
            rule = re.sub("{\w*\|c}", "([a-zA-Z]+)", rule)

        rule = "^" + rule + '$'

        match = re.match(rule, path)
        if match:
            route_parameters = {}
            if len(key_list) > 0:
                route_parameters = dict(zip(key_list, match.groups()))
            return Router.Match(route_parameters)

        return None
