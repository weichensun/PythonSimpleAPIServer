#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_worker import Base_Worker
import re
import imp
import sys
import inspect

class Worker_Loader:

    @classmethod
    def load(self, module_path):
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
            print(sys.exc_info())

        return worker
