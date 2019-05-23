
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, './../')

from server import Server
from server.worker import Worker

class HelloWorker(Worker):
    def do_GET(self):
        return self.responseOK("HelloWorld !")

    def do_POST(self):
        data = self.getRequestBody()
        print(data)
        return self.responseOK("OK")

class ObjectWorker(Worker):
    def do_GET(self):
        object_id = self.route_params['id']
        return self.responseOK("Object id = %s" % object_id)

class UrlQueryWorker(Worker):
    def do_GET(self):
        return self.responseOK({"id":self.get_url_query('id')})

class FileWorker(Worker):
    def do_GET(self):
        return self.responseFile('./image/lenna.png')

class NoFileWorker(Worker):
    def do_GET(self):
        return self.responseFile('./image/noimg.png')

def auth(handler, route_params, url_query):
    pass
#    return True
#    return {
#        'code': 401,
#        'reason': 'Unauthorized'
#    }

server = Server()
server.set_auth_function(auth)
server.add_worker("/", HelloWorker)
server.add_worker("/query", UrlQueryWorker)
server.add_worker("/object/{id}", ObjectWorker)
server.add_worker("/img", FileWorker)
server.add_worker("/noimg", NoFileWorker)
server.run(threading=True, debug=True)
