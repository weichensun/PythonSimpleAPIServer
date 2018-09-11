#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_worker import BaseWorker

class Object(BaseWorker):

    def do_GET(self):
        return self.replyOK("The object id is %s." % self.get_route_parameter("id"))
