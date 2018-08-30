#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_route import BaseRoute

class Route(BaseRoute):

    def set_route(s):
        s.add('/', 'app.api.index/Index')
        s.add('/task', 'app.api.task')
        s.add('/object/{id|n}', 'app.api.object')
