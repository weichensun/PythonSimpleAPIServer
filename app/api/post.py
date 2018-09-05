#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core.base_worker import Base_Worker

class Post(Base_Worker):

    def do_POST(self):
        return self.replyOK("OK")
