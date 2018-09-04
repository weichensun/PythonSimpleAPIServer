#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_worker import Base_Worker

class Post(Base_Worker):

    def do_POST(self):
#        print self.request_body
        with open('fff.png', 'wb') as f:
            f.write(self.request_body['data'])
        
        return self.replyOK("OK")
