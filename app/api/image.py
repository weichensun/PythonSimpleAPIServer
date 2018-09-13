#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.http_worker import HttpWorker

class Image(HttpWorker):

    def do_GET(self):
        path = 'image/lenna.png'
        return self.replyFile(path)
