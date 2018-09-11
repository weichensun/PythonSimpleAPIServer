#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_worker import BaseWorker

class HelloWorld(BaseWorker):

    def do_GET(self):
        return self.replyOK('Hello World!')
