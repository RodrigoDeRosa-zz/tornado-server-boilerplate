from tornado.ioloop import IOLoop

from src.database.mongo import Mongo
from src.jobs.scheduler import Scheduler
from src.server.http_server_factory import HTTPServerFactory
from src.server.tornado_application import ApplicationFactory
from src.utils.command_line.argument_parsing_utils import ArgumentParsingUtils
from src.utils.logging.logger import Logger


class Server:

    @classmethod
    def start(cls):
        # Read command line arguments
        port, ssl, processes, env, db_data, logging_data = ArgumentParsingUtils.parse_arguments()
        # Configure application logging
        Logger.set_up(**logging_data)
        # Create application and server
        tornado_application = ApplicationFactory.tornado_app()
        HTTPServerFactory.create(tornado_application, port, ssl).start()
        # Connect to MongoDB server
        Mongo.init(**db_data)
        # This is done so that every incoming request has a pointer to the database connection
        tornado_application.settings['db'] = Mongo.get()
        # Configure task scheduler
        Scheduler.example_set_up()
        # Start event loop
        Logger(cls.__name__).info(f'Listening on http://localhost:{5000}.')
        IOLoop.current().start()
