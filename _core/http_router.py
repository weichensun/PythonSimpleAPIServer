#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import imp
import re
import inspect
from _core.http_worker import HttpWorker

class Match():
    def __init__(self, route_parameters):
        self.route_parameters = route_parameters

class HttpRouter():

    @classmethod
    def get_worker_by_path(self, path, request_handler):
        worker = None
        try:
            router = __import__('app.route', fromlist = [''])
            router = imp.reload(router)
            for pattern, worker_module_path in router.get_route_list():
                matched = self.match_pattern_and_path(pattern, path)
                if matched:
                    worker_class = self.get_worker_class(worker_module_path)
                    worker = worker_class(matched.route_parameters, request_handler)
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
            rule = re.sub("{\\w*}", r"([\\'\\.\\*\\w+!(),\\-\\$\\%]+)", rule)
            rule = re.sub("{\\w*\\|n}", r"(\\d+)", rule)
            rule = re.sub("{\\w*\\|c}", r"([a-zA-Z]+)", rule)

        rule = "^" + rule + '$'

        match = re.match(rule, path)
        if match:
            route_parameters = {}
            if len(key_list) > 0:
                route_parameters = dict(zip(key_list, match.groups()))
            return Match(route_parameters)

        return None

    @classmethod
    def get_worker_class(self, module_path):
        worker = None
        try:
            class_name = ''
            if '/' in module_path:
                match = re.match("([^*\/]+)/([^*\/]+)", module_path)
                module_path = match.groups()[0]
                class_name = match.groups()[1]

            from_list = module_path.rfind('.')
            module = __import__(module_path)
            module = __import__(module_path, fromlist=[ from_list ] )
            module = imp.reload(module)

            if class_name != '':
                obj = getattr(module, class_name)
                if issubclass(obj, HttpWorker):
                    worker = obj
            else:
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name != HttpWorker.__name__ and issubclass(obj, HttpWorker):
                        worker = obj
                        break

        except:
            print(sys.exc_info())

        return worker
