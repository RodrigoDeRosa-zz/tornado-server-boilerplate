from tornado.ioloop import IOLoop

from src.database.mongo import Mongo
from src.jobs.scheduler import Scheduler
from src.server.application_context import ApplicationContext
from src.server.http_server_factory import HTTPServerFactory
from src.server.tornado_application import ApplicationFactory
from src.utils.command_line.argument_parsing_utils import ArgumentParsingUtils
from src.utils.concurrency.lock_manager import LockManager
from src.utils.logging.logger import Logger


class Server:

    @classmethod
    def start(cls):
        # Read command line arguments
        context: ApplicationContext = ArgumentParsingUtils.parse_arguments()
        # Configure application logging
        Logger.set_up(context.logging_data)
        # Create application and server
        tornado_application = ApplicationFactory.tornado_app()
        HTTPServerFactory.create(tornado_application, context).start(context.process_number)
        # Connect to MongoDB server
        Mongo.init(context.db_data)
        # This is done so that every incoming request has a pointer to the database connection
        tornado_application.settings['db'] = Mongo.get()
        # Configure task scheduler.
        # Beware! This will be run on every process, be careful if using multi process. Check ConcurrentExampleJob
        Scheduler.example_set_up()
        # Connect to distributed lock client. This is the same as with the database
        tornado_application.settings['lock_manager'] = LockManager(context.lock_server_data)
        # Start event loop
        Logger(cls.__name__).info(f'Listening on {"https" if context.ssl else "http"}://localhost:{context.port}.')
        IOLoop.current().start()
