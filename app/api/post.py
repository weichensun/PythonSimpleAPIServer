#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.http_worker import HttpWorker

class Post(HttpWorker):

    def do_POST(self):
        print(self.get_request_body())
        return self.replyOK("OK")
