#!/usr/bin/python
# -*- coding: utf-8 -*-

from _core import worker_base

class API_Worker( worker_base.API_Worker_Base ):

    def do_GET( self ):
        self.reply( 'Hello World', 'text/html', 200 )

