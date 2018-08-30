#!/usr/bin/python
# -*- coding: utf-8 -*-

import imp
import re
from _core.base_worker import Base_Worker
from _core.worker_loader import Worker_Loader

class Router ():

    class PathMatched():
        def __init__(self, url_variables):
            self.url_variables = url_variables

    def __init__(self):
        self.worker_loader = Worker_Loader()

    def get_worker_by_path(self, path):
        worker = None
        try:
            route = __import__('app.route', fromlist = ['app'])
            route = imp.reload(route)
            route_rules = route.get()

            for rule in route_rules.keys():
                matched = self.match_rule_and_path(rule, path)
                if matched:
                    worker = self.load_worker(route_rules[path])
                    break

        except ImportError:
            pass

        return worker

    def match_rule_and_path(self, rule, path):
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
            return Router.PathMatched(url_variables)

        return None


    def load_worker(self, module_info):
        worker = None
        try:
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
