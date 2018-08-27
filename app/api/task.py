#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core import worker_base
import time

class API_Worker(worker_base.API_Worker_Base):

    def do_GET( self ):
        # We use ThreadedHTTPServer
        # A long task will not block other service request
        time.sleep(10)
        self.reply('Complete', 'text/html', 200)
