#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.http_worker import HttpWorker

class HelloWorld(HttpWorker):

    def do_GET(self):
        return self.replyOK('Hello World!')
