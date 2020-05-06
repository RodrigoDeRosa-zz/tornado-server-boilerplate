from src.request_handlers.health_check_handler import HealthCheckHandler


class Router:

    # Dictionary to map routes to Tornado RequestHandler subclasses
    ROUTES = {
        '/ping': HealthCheckHandler,
    }

    @classmethod
    def routes(cls):
        """ Get routes with their respective handlers"""
        return [(k, v) for k, v in cls.ROUTES.items()]
