from src.request_handlers.custom_request_handler import CustomRequestHandler


class ExampleCORSHandler(CustomRequestHandler):

    CORS_ENABLED = True
    SUPPORTED_METHODS = ['OPTIONS', 'POST', 'GET']

    async def post(self):
        pass

    async def get(self):
        pass
