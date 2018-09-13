#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_route_list():
    return [
        ('/', 'app.api.hello_world/HelloWorld'),
        ('/task', 'app.api.task'),
        ('/object/{id|n}', 'app.api.object'),
        ('/post', 'app.api.post'),
        ('/image', 'app.api.image'),
    ]
