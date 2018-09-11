#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_route import BaseRoute

class Route(BaseRoute):

    def set_route(s):
        s.add('/', 'app.api.hello_world/HelloWorld')
        s.add('/task', 'app.api.task')
        s.add('/object/{id|n}', 'app.api.object')
        s.add('/post', 'app.api.post')
        s.add('/image', 'app.api.image')
