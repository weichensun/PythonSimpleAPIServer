## About

A small improved http server framework base on Python BaseHTTPServer

#### Features
	Working on python2 and python3
	Use threading to process multiple requests (No blocking)
	Support HTTPS
	Use simple route to load worker
	Dynamic load worker class
	
	[coming] compress response

#### Support most of the HTTP methods
	
	GET	-
	POST	-
	PUT	-
	DELETE	-

## Quick Start:
#### Start Server
	python server.py
	
#### Connect to Server
	$ curl localhost:5000

	> HelloWorld!

## Route Settings

### Add New Route

To set route, just need to modify app/route.py and specify route and worker
	
To add a route, just simply add
	
	self.add({ROUTE}, {WORKER_MODULE})
	
under def set_route(self) method

### Route Settings

#### Route Parameters

This framework supports route parameter. If you want to identify

	e.g: /object/{id|n}
	e.g: /object/{type}/{id|n}

Default 

	'/request/path/{VAR_NAME}'
	e.g: /request/path/var_name_123

Filter Number only

	'/request/path/{VAR_NAME|n}'
	e.g: /request/path/1234
	
Filter Charactor only

	'/request/path/{VAR_NAME|c}'
	e.g: /request/path/name


#### Worker

The worker definition

	{WORKER_MODULE_PATH}(/{WORKER_CLASS_NAME})

Supply module path and class name (class name is optional)

	'app.api.index/Index'

So, if only module path is supplied like

	'app.api.index'

The loader will automatically load the first worker class under the module
	
	
