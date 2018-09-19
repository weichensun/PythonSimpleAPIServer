#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.http_worker import HttpWorker

class Post(HttpWorker):

    def do_POST(self):
        print(self.get_post_data())
        return self.replyOK("OK")
