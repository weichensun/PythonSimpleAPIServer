#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_worker import BaseWorker

class Post(BaseWorker):

    def do_POST(self):
        return self.replyOK("OK")
