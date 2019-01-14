# About

This project is base on pure Python's BaseHTTPServer, to minimize dependency

Below will be the spec of the newer version of SimplePythonHttpServer

## Features
1. Working on python2.7 and up to python3.7
2. Use threading to process multiple requests (No blocking)
3. Support HTTPS
4. Use worker class make service more dynamic
5. URL path variable
6. Global Middleware support
7. ~~Dynamic load worker class~~ *
8. ~~Dynamic add route path~~


## Sample Code

```python
from server import Server
from server.worker import Worker



class HelloWorker(Worker):
    def do_GET(self):
        return self.responseOK("HelloWorld !")



class ObjectWorker(Worker):
    def do_GET(self):
        object_id = self.route_params['id']
        return self.responseOK("Object id = %s" % object_id)



server = Server()
server.add_worker("/", HelloWorker)
server.add_worker("/object/{id}", ObjectWorker)
server.run(threading=True, debug=True)
```

## More Tutorial and Codes
* Server Functions
    * Setup Routing
    * Run with Threading
    * SSL Setup
    * Debug
    * Middleware
* Worker Functions
    * Get Request Data
        * Read Request Header
        * Read Request URL Param
        * Read POST Data/File
    * Set Responses Data
        * Set Reply Data
        * Set Reply Headers
        * Set Reply File


## Story with Python's BaseHTTPServer

More see: [Wiki](https://github.com/weichensun/SimplePythonHttpServer/wiki)
	
