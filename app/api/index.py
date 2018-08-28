#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_worker import Base_Worker

class Index(Base_Worker):

    def do_GET( self ):
        return self.replyOK('Hello World!')
