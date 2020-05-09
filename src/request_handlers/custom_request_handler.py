from json import dumps, loads

from tornado.web import RequestHandler

from src.database.mongo import Mongo
from src.model.errors.business_error import BusinessError
from src.utils.concurrency.lock_manager import LockManager
from src.utils.gzip_utils import GzipUtils
from src.utils.logging.logger import Logger
from src.utils.mapping_utils import MappingUtils


class CustomRequestHandler(RequestHandler):

    INTERNAL_ERROR_MESSAGE = 'Internal Server Error. ' \
                             'Our best engineers were [probably] notified and are [probably] running to fix it.'
    CORS_ENABLED = False

    def prepare(self):
        # This is needed so that every request can access globally to the database or lock server
        Mongo.set(self.settings['db'])
        LockManager.set(self.settings['lock_manager'])

    def data_received(self, chunk):
        pass

    def options(self, **kwargs):
        """ Generic options handler for browser requests. """
        self.make_response(status_code=204)

    def make_error_response(self, status_code, message):
        """ Create a common error response. """
        self.get_logger().error(f'{status_code} | {message}')
        self.set_status(status_code)
        response = {'status': status_code, 'message': message}
        self.write(response)

    def make_response(self, response_body=None, status_code=200):
        """ Create a common success response. """
        self.set_status(status_code)
        # Set default JSON content header
        self.set_header('Content-Type', 'application/json')
        # Only add headers for those handlers that accept CORS
        if self.CORS_ENABLED:
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Headers', '*')
            self.set_header('Access-Control-Allow-Methods', ', '.join(self.SUPPORTED_METHODS))
        # Null response is also accepted
        if response_body is not None:
            # This is in case of gzip encoding
            if GzipUtils.accepts_gzip_compression(self.request.headers):
                self.set_header('Content-Encoding', 'gzip')
                self.write(GzipUtils.gzip_compress(str(response_body)))
            else:
                # The following is done to accept List responses (Tornado doesn't accept them by default)
                json_response = response_body if not isinstance(response_body, str) else loads(response_body)
                self.write(dumps(json_response))

    def _parse_body(self):
        try:
            return MappingUtils.decode_request_body(self.request.body)
        except RuntimeError:
            raise BusinessError(f'Invalid request body {self.request.body}', 400)

    def get_logger(self):
        return Logger(self.__class__.__name__)
