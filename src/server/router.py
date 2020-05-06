from src.request_handlers.crud_example.example_crud_handler import ExampleCRUDHandler
from src.request_handlers.cors_example.example_cors_handler import ExampleCORSHandler
from src.request_handlers.health_check_handler import HealthCheckHandler
from src.request_handlers.locking_example.example_locking_handler import ExampleLockingHandler


class Router:

    # Dictionary to map routes to Tornado RequestHandler subclasses
    ROUTES = {
        '/ping': HealthCheckHandler,
        '/resources/?(?P<resource_id>[^/]+)?': ExampleCRUDHandler,
        '/locking/?(?P<lock_id>[^/]+)?': ExampleLockingHandler,
        '/cors': ExampleCORSHandler
    }

    @classmethod
    def routes(cls):
        """ Get routes with their respective handlers"""
        return [(k, v) for k, v in cls.ROUTES.items()]
