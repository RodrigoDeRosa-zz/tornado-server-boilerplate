from motor.motor_tornado import MotorClient

from src.utils.logging.logger import Logger


class Mongo:
    """ MongoDB access point. """

    __CLIENT = None
    DB = None

    @classmethod
    def init(cls, host, port, db_name, user, password):
        """ Create database with asynchronous connector."""
        cls.get_logger().info('Establishing database connection...')
        uri = cls.__create_uri(host, port, user, password, db_name)
        # Create db client
        cls.__CLIENT = MotorClient(uri)
        cls.DB = cls.__CLIENT.get_default_database()

    @classmethod
    def set(cls, db):
        # The received db will always be the same object so concurrence won't be a problem.
        # This is just for a more comfortable usage
        cls.DB = db

    @classmethod
    def get(cls):
        return cls.DB

    @classmethod
    def __create_uri(cls, host, port, user, password, db_name):
        """ Generates database URI"""
        # Create auth string from parameters
        auth = f'{user}:{password}@' if user and password else ''
        # Create database URI
        return f'mongodb://{auth}{host}:{port}/{db_name}?retryWrites=false'

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
