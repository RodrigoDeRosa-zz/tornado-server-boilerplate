from argparse import ArgumentParser

from src.server.application_context import ApplicationContext, DatabaseData, LoggingData, LockServerData


class ArgumentParsingUtils:

    @classmethod
    def parse_arguments(cls) -> ApplicationContext:
        """ Get environment from program argument_parsing. tornado.options could be used instead of ArgumentParser. """
        parser = ArgumentParser()
        # Set up argument values
        parser.add_argument('--proc', default=1, type=int, help='Number of processes. 0 is one per CPU')
        parser.add_argument('--port', default=5000, type=int, help='Port where application will listen')
        parser.add_argument('--env', default='dev', help='Current execution environment')
        parser.add_argument('--ssl', default=False, action='store_true', help='SSL switch')
        # Database related args
        parser.add_argument('--db_host', default='localhost', help='MongoDB host')
        parser.add_argument('--db_port', default=27017, type=int, help='MongoDB port')
        parser.add_argument('--db_name', default='tornado_boilerplate', help='MongoDB database name')
        parser.add_argument('--db_user', default=None, help='MongoDB authentication user')
        parser.add_argument('--db_password', default=None, help='MongoDB authentication password')
        # Logging related args
        parser.add_argument('--log_host', default=None, help='UDP logging server hostname')
        parser.add_argument('--log_port', default=None, type=int, help='UDP logging server port')
        # Lock server related args
        parser.add_argument('--lock_server', default=False, action='store_true', help='Distributed lock server enabler')
        parser.add_argument('--lock_server_host', default=None, help='Distributed lock server hostname')
        parser.add_argument('--lock_server_port', type=int, default=2379, help='Distributed lock server port')
        # Get program argument_parsing
        args = parser.parse_args()
        # Create DB data dictionary
        db_data = DatabaseData(
            host=args.db_host,
            port=args.db_port,
            name=args.db_name,
            user=args.db_user,
            password=args.db_password
        )
        # UDP logging parameters
        logging_data = LoggingData(
            host=args.log_host,
            port=args.log_port
        )
        # Lock server parameters
        lock_server_data = LockServerData(
            enabled=args.lock_server_host,
            host=args.lock_server_host,
            port=args.lock_server_port
        )
        # Build application context
        return ApplicationContext(
            process_number=args.proc,
            port=args.port,
            env=args.env,
            ssl=args.ssl,
            db_data=db_data,
            logging_data=logging_data,
            lock_server_data=lock_server_data
        )
