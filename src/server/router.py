from src.request_handlers.crud_example.example_crud_handler import ExampleCRUDHandler
from src.request_handlers.example_cors_handler import ExampleCORSHandler
from src.request_handlers.health_check_handler import HealthCheckHandler


class Router:

    # Dictionary to map routes to Tornado RequestHandler subclasses
    ROUTES = {
        '/ping': HealthCheckHandler,
        '/resources/?(?P<resource_id>[^/]+)?': ExampleCRUDHandler,
        '/cors': ExampleCORSHandler
    }

    @classmethod
    def routes(cls):
        """ Get routes with their respective handlers"""
        return [(k, v) for k, v in cls.ROUTES.items()]
