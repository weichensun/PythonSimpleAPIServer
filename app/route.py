#!/usr/bin/python
# -*- coding: utf-8 -*-

# Route rules definition
#
# 1, In string
#
#   route["{REQUEST_PATH}"] = "{MODULE_PATH}/{CLASS_NAME}"
#   route["{REQUEST_PATH}"] = "{MODULE_PATH}"
#
# 2, In array
#
#   route["{REQUEST_PATH}"] = ["{MODULE_PATH}", "{CLASS_NAME}"]
#   route["{REQUEST_PATH}"] = ["{MODULE_PATH}"]
#
# If the class name is not supplied, the loader will find the class in the module
#

def get():

    route = {}
    route['/']          = 'app.api.index/Index'
    route['/task']      = ['app.api.task']

    return route
