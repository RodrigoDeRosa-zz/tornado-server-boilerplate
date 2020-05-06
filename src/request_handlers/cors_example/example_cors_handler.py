from src.request_handlers.custom_request_handler import CustomRequestHandler


class ExampleCORSHandler(CustomRequestHandler):

    CORS_ENABLED = True
    SUPPORTED_METHODS = ['OPTIONS', 'POST', 'GET']

    async def post(self):
        self.make_response({'postedSomething': True})

    async def get(self):
        self.make_response({'aKey': 'aValue'})
