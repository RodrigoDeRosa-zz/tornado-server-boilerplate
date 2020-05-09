from src.model.errors.business_error import BusinessError
from src.request_handlers.custom_request_handler import CustomRequestHandler
from src.service.example_client_service import ExampleClientService


class ExampleClientHandler(CustomRequestHandler):
    """ Example handler for requests that require making requests to an external service. """

    SUPPORTED_METHODS = ['GET']

    async def get(self):
        try:
            response = await ExampleClientService.do_request()
            self.make_response(response)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)
