
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

class RouteParam(Worker):
    def do_GET(self):
        return self.responseOK(self.get_route_param("param"))

class UrlQuery(Worker):
    def do_GET(self):
        return self.responseOK({"id":self.get_url_query('id')})

class Header(Worker):
    def do_GET(self):
        return self.responseOK(self.get_request_header("x-some-header"))

class File(Worker):
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
server.add_worker("/query", UrlQuery)
server.add_worker("/route/{param}", RouteParam)
server.add_worker("/header", Header)
server.add_worker("/file", File)
server.add_worker("/noimg", NoFileWorker)
server.run(threading=True, debug=True)
