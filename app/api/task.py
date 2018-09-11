#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_worker import BaseWorker
import time

class task(BaseWorker):

    def do_GET(self):
        # We use ThreadedHTTPServer
        # A long task will not block other service request
        time.sleep(5)
        return self.replyOK('Task Complete')
