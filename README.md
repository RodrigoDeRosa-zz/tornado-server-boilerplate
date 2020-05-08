# Tornado Server Boilerplate

> Python Tornado server boilerplate with Logging (console, file and UDP), Scheduling, CORS, MongoDB connection and HTTPS 
support, docker-compose configuration for deployment and Heroku support, as well as a local startup system with venv.
Instructions on how it works will be found below.

## Table of contents

* [Execution methods](#execution-methods)
    * [Local execution with venv](#local-execution-with-venv)
    * [Docker](#docker)
    * [Heroku](#heroku)
* [Command line parameters](#command-line-parameters)
    * [Basic application parameters](#basic-application-parameters)
    * [Logging parameters](#logging-parameters)
    * [Database parameters](#database-parameters)
    * [Distributed lock server parameters](#distributed-lock-server-parameters)
* [HTTPS](#https)
* [Request handlers](#request-handlers)
    * [Custom Request Handler](#custom-request-handler)
    * [HTTP verb handling](#http-verb-handling)
    * [Path parameters](#path-parameters)
    * [Sync vs Async](#sync-vs-async)
* [Routing](#routing)
* [Views](#views)
* [CORS](#cors)
* [Logging](#logging)
    * [Log Handlers](#log-handlers)
    * [Logger Instancing](#logger-instancing)
    
**NOTE:** There are still a lot of things to cover in this readme!! It's a WIP!

## Execution methods

### Local execution with venv

#### Requirements
In this case, to start the application you'll have to execute `make prepare` and `make run`. If you look at the code
inside `Makefile`, you'll see the requirements for this execution methods are:

* `python3.8`
* `python3-pip`
* `python3.8-venv`

In order to simplify the installation of these packages, `Makefile` has the command `install-requirements` which does
exactly that. You may need to execute the command as superuser: `sudo make install-requirements`.

Nevertheless, this is not enough; given that the server will try to connect to a MongoDB server, you must make sure you
have said [MongoDB](https://www.mongodb.com/) server running on port `27017` (if you will run the Tornado server on 
default parameters).

#### Database
As you can see in the `Makefile`, this execution receives no parameters; this means it will use all default values for
database connection. As mentioned before, this means the Tornado server will try to create a database called 
`tornado_boilerplate` in a MongoDB server running on port `27017`. If you wanted to change this configuration, check the
parameter section of this document.

#### Distributed lock server
This execution method has this functionality turned off by default. If you wanted to turn it on, you should set the
flag as a parameter. Make sure you have installed and running an [etcd](https://etcd.io/) server. The default port is
`2379`, but you can define your own in the parameters.

#### Port and protocol
As explained previously, this execution method will use the default parameters; this means that the Tornado server will 
start on port `5000` in `HTTP` mode. If you wanted to change this, refer to the parameter section.

#### Number of processes
The default number of processes is 1; you can change this in the application parameters.

---
### Docker

#### Requirements
To run the server with [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/), you'll 
need to have the following packages installed in your system:

* `docker`
* `docker-compose`

Once you have these two, you'll be able to run the Tornado server in your machine by executing 
`docker-compose up --build`.

#### Database
A MongoDB server will be started as a service within the docker-compose context and the Tornado server will connect
to it on `mongodb:27017`, which is the hostname inside the Docker container and the default MongoDB port.

#### Distributed lock server
In this execution method, an etcd server will be running within the docker-compose context and the Tornado server will
connect to it on `etcd:2379`, which is the hostname inside of the Docker container and the default etcd port.

#### Port and protocol
The Tornado server will start on port `5000` in `HTTP` mode. To change the listening port, check the `ports` field
in the `server` service within `docker-compose.yml`.

#### Number of processes
In this case, the Tornado server will be running on 2 processes; this is just to show the `ConcurrentExampleJob`
behaviour and it can be modified in the `Dockerfile`. Check the parameter section for information on how each of them
works.

---
### Heroku
This boilerplate is ready to be deployed on [Heroku](https://www.heroku.com/) with 
[mLab](https://elements.heroku.com/addons/mongolab) support. For a correct connection to the MongoDB server, make sure
you define the following environment properties on your Heroku application:

* `MONGODB_HOST`
* `MONGODB_PORT`
* `MONGODB_USER`
* `MONGODB_PASSWORD`
* `MONGODB_NAME`

All of these can be taken from the `MONGO_URI` environment variable you'll already have from adding mLab to your Heroku 
application.

## Command line parameters
In this section, command line parameter parsing and purpose is covered. Everything that is explained here can be found
within the code, in `src.utils.command_line.argument_parsing_utils.ArgumentParsingUtils`.

Argument parsing logic is handled by the `argparse` library; you can read about how it works in Python's official
[docs](https://docs.python.org/3/library/argparse.html). By using this library, we automatically have access to a 
description of the accepted command line parameters by running `python server.py -h`.

In the following sections we will detail every parameter the application accepts and what do they do.

### Basic application parameters
There are five parameters considered basic:
* `--proc PROC`: Determines the number of Tornado servers that will be started, each of these servers in a different 
process. The default value is `1`; `--proc 0`  will run as many server processes as cores the system running the 
application has.
* `--port PORT`: Determines the port where the server will be running. The default value is `5000`. If your are running 
the server on Docker, make sure you change the exposed port.
* `--env ENV`: Environment variable. Not currently used but it could be used across the application to determine 
different ways of resolving issues, depending on the environment.
* `--ssl`: SSL switch. When this parameter is passed to the application, it will run on SSL mode. See SSL section to 
understand what this means.

### Logging parameters
This set of parameters are used specifically to log to an UDP logging server.
* `--log_host HOST`: Name of the UDP logging server host. `None` by default.
* `--log_port PORT`: Port where the UDP logging server is running. `None` by default.

To understand what happens when this parameters are not null, check the Logging section.

### Database parameters
Given this boilerplate server comes with MongoDB support, it is possible to pass as command line argument some of the
database server's data. 
* `--db_host HOST`: Name of the server where the MongoDB server is running. Default is `localhost`.
* `--db_port PORT`: Port where the MongoDB server is running. Default is `27017`.
* `--db_name NAME`: Name of the database to use. Default is `tornado_boilerplate`.
* `--db_user USER`: Username for database authentication. Default is `None`.
* `--db_password PASSWORD`: Password for database authentication. Default is `None`.

As mentioned previously, all of these parameters need to be set in Heroku application settings in order to connect to
an mLab MongoDB server.

### Distributed lock server parameters
If you wanted to use an etcd server as a distributed lock server, you need to pass the following parameters:
* `--lock_server`: Switch that, when passed, indicates that a distributed lock server will be used.
* `--lock-server-host`: Name of the host where the etcd server is running.
* `--lock-server-port`: Port where the etcd server is running. Default is `2379`.

## HTTPS
The server is run on HTTP by default but, as previously mentioned, it can be run on HTTPS mode if the `--ssl` parameter
is passed on startup.

SSL configuration is set on the application on `src.server.http_server_factory.HTTPServerFactory`. As you can see, both
a `certfile` and a `keyfile` are needed; these two files should be located on the `/keys/` directory. This boilerplate
has two empty files as an example.

## Request Handlers
All incoming requests in tornado are handled by an specific class that extends from `RequestHandler`. In order to
centralize certain common methods, this boilerplate has an implementation of a `RequestHandler` subclass found in 
`src.request_handlers.custom_request_handler.CustomRequestHandler` .

### Custom Request Handler
This class should be used as the parent class of all newly created request handlers; every example in this boilerplate
is a subclass of it.

In this class, you will find a centralization of both successful and erroneous response handling; also, it has a generic
method for handling `OPTIONS` requests, a `prepare()` method that is executed each time a request enters the server and
a request body mapper that transforms the incoming request body into a dictionary.

### HTTP verb handling
Every new subclass of `CustomRequestHandler` will be associated to an specific route and will answer every incoming
request to said route. In every request handler there are two things that must be defined:
 
* The `SUPPORTED_METHODS` attribute, which is a list of HTTP verbs and that defaults to accept every verb. Every non
included verb will return an HTTP code `405`, for `Method Not Allowed`.
* A class method for each of the verbs; for example, `def post(self):` to handle `POST` requests.

### Path parameters
Path parameters are defined when routing and are needed in all request handling methods, even if they are not used. 
Explanation on how to define them will be found in the routing section.
 
### Sync vs Async
All request handling methods can be either synchronous (`def post(self):`) or asynchronous (`async def post(self):`);
this means that requests can be handled both with common Python methods and with Python coroutines. In this boilerplate
you can see that both the `HealthCheckHandler` and the `ExampleViewHandler` use a synchronous method and all the other 
handlers use Python coroutines.

Given Tornado's ability to handle coroutines, it is recommended for you to answer requests with coroutines, in order to
exploit this ability to the maximum.

## Routing
The relationship between paths and request handlers is defined in `src.server.router.Router`; here, a dictionary that
relates each path with it's handler is created and is the used in the creation of the Tornado application in 
`src.server.application_factory.ApplicationFactory`.

Path params are set in the path definition; an example of a path definition with an optional query param is 
`/resources/?(?P<resource_id>[^/]+)?`. The name on the place holder will also be the name the request handling methods
will receive when called.

## Views
This boilerplate also includes an example of how to serve HTML pages. The settings on the locations of the needed 
resources are on `src.server.application_factory.ApplicationFactory`. It is important to note that these relative paths
are related to the class from where they are requested; in this case, it would be from 
`src.request_handlers.view_example.ExampleViewHandler`.

In this particular example, resources are located in the `/views/` folder, divided in `templates` and `static`. In the
first one there is an example HTML file and in the second one a CSS example.

## CORS
When using this server as a backend for a front end application, you should take into consideration setting the CORS
headers. In this boilerplate, CORS can be enabled for a particular `RequestHandler` by overriding the 
`CustomRequestHandler` class attribute `CORS_ENABLED`; if this attribute is `True`, CORS headers will be set on every
response.

An example of a CORS supporting handler can be found in `src.request_handlers.cors_example.ExampleCORSHandler`.

**NOTE:** It is also possible that you will need to accept the `OPTIONS` verb for this cases; this is handled in 
`src.request_handlers.custom_request_handler.CustomRequestHandler`.

## Logging
Logging is handled by Python's [logging](https://docs.python.org/3/library/logging.html) library. The `Logger` class can
be found in `src.utils.logging.logger`.

This class has a few class attributes that are used as basic configuration for the logging system; those are:
* `FORMATTING_STRING`: The format in which every log line will be displayed.
* `LOGGING_LEVEL`: Minimum logging level that is displayed in the logs.
* `LOGGING_FILE_NAME`: Name of the file where the logs will be stored.
* `MAX_BYTE`: Maximum size of the log file.
* `BACKUP_COUNT`: Number of files of the maximum size that will be stored using a rotating file method.

### Log handlers
The current configuration of the `Logger` class logs both to the console and to a file placed in the `/logs/` directory,
which will be created on startup if it doesn't exist, as well as a file named `server.log`. This is, both a 
`StreamHandler` and a `RotatingFileHandler` are used by default.

As mentioned in the parameter section, if values for `--log_host` and `--log_port` are passed, a `SysLogHandler` will be
also added, enabling UDP logging.

### Logger instancing
To get an instance of `Logger`, you simply need to do `logger = Logger('aName')`, the value passed as parameter will be
the one filling the `name` field in the logging format. This class could be eventually extended to be a multiton, to
avoid creating an instance every time you need to log.