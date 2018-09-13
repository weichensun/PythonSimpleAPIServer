#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.http_worker import HttpWorker

class Object(HttpWorker):

    def do_GET(self):
        return self.replyOK("The object id is %s." % self.get_route_parameter("id"))
