#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, './../')

from server import Server
from server.router import Route, Router
from server.worker import Worker

class HelloWorker(Worker):
    def do_GET(self):
        return self.responseOK("HelloWorld !")

    def do_POST(self):
        data = self.get_request_body()
        return self.responseOK(data)

class ObjectWorker(Worker):
    def do_GET(self):
        object_id = self.route_params['id']
        return self.responseOK("Object id = %s" % object_id)

class FileWorker(Worker):
    def do_GET(self):
        return self.responseFile('./image/lenna.png')


server = Server()
server.add_worker("/", HelloWorker)
server.add_worker("/object/{id}", ObjectWorker)
server.add_worker("/image", FileWorker)
server.run(threading=True, debug=True)
