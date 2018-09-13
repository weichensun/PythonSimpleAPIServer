#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.http_worker import HttpWorker

class Post(HttpWorker):

    def do_POST(self):
        return self.replyOK("OK")
