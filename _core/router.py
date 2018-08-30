#!/usr/bin/python
# -*- coding: utf-8 -*-

import imp
import re
from _core.base_worker import Base_Worker
from _core.worker_loader import Worker_Loader

class Router ():

    class Match():
        def __init__(self, url_variables):
            self.url_variables = url_variables

    def __init__(self):
        self.worker_loader = Worker_Loader()

    def get_worker_by_path(self, path):
        worker = None
        try:
            route = __import__('app.route', fromlist = ['app'])
            route = imp.reload(route)
            route = route.Route()

            for route in route.route_list:
                matched = self.match_pattern_and_path(route.pattern, path)
                if matched:
                    worker = self.worker_loader.load(route.worker_module_path)
                    break

        except ImportError:
            pass

        return worker

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
            url_variables = {}
            if len(key_list) > 0:
                url_variables = dict(zip(key_list, match.groups()))
            return Router.Match(url_variables)

        return None
