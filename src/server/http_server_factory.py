from tornado.httpserver import HTTPServer
from os.path import abspath, join, dirname

from tornado.web import Application


class HTTPServerFactory:

    KEYS_DIR_PATH = f'{abspath(join(dirname(__file__), "../../../"))}/keys/'

    @classmethod
    def create(cls, application: Application, port: int, ssl: bool) -> HTTPServer:
        # HTTPS certificate configuration
        ssl_options = {
            'certfile': f'{cls.KEYS_DIR_PATH}public-key.pem',
            'keyfile': f'{cls.KEYS_DIR_PATH}private-key.pem'
        } if ssl else None
        # Server creation
        server = HTTPServer(application, ssl_options=ssl_options)
        server.bind(port)
        return server
