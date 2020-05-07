# Tornado Server Boilerplate

> Python Tornado server boilerplate with Logging (console, file and UDP), Scheduling, CORS, MongoDB connection and HTTPS 
support, docker-compose configuration for deployment and Heroku support, as well as a local startup system with venv.
Instructions on how it works will be found below.

## Table of contents

* [Execution methods](#Execution methods)
    * [Local execution with venv](#local execution with venv)
    * [Docker](#docker)
    * [Heroku](#heroku)

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

### Heroku

This boilerplate is ready to be on [Heroku](https://www.heroku.com/) with 
[mLab](https://elements.heroku.com/addons/mongolab) support. For a correct connection to the MongoDB server, make sure
you define the following environment properties on your Heroku application:

* MONGODB_HOST
* MONGODB_PORT
* MONGODB_USER
* MONGODB_PASSWORD
* MONGODB_NAME

All of these can be taken from the `MONGO_URI` environment variable you'll already have from adding mLab to your Heroku 
application.

