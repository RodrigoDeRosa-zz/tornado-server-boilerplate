from src.request_handlers.custom_request_handler import CustomRequestHandler


class HealthCheckHandler(CustomRequestHandler):
    """ Handler for health checks. """

    SUPPORTED_METHODS = ['GET']

    def get(self):
        self.make_response(status_code=200)

    def _log(self):
        # Avoid logging request data on health checks to avoid filling log files
        pass
