from src.model.errors.business_error import BusinessError
from src.request_handlers.crud_example.mappers.example_request_mapper import ExampleRequestMapper
from src.request_handlers.crud_example.mappers.example_response_mapper import ExampleResponseMapper
from src.request_handlers.custom_request_handler import CustomRequestHandler
from src.service.example_crud_service import ExampleCRUDService


class ExampleCRUDHandler(CustomRequestHandler):
    """ Example handler for CRUD operations on an specific resource type. """

    SUPPORTED_METHODS = ['GET', 'POST', 'PATCH', 'DELETE']

    async def get(self, resource_id):
        try:
            if not resource_id:
                resources = await ExampleCRUDService.retrieve_all()
                self.make_response(ExampleResponseMapper.map_many(resources))
            else:
                resource = await ExampleCRUDService.retrieve(resource_id)
                self.make_response(ExampleResponseMapper.map(resource))
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def post(self, resource_id):
        try:
            resource = ExampleRequestMapper.map_creation(self._parse_body())
            await ExampleCRUDService.add(resource)
            # This service only returns an HTTP 200
            self.make_response(status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def patch(self, resource_id):
        try:
            resource = ExampleRequestMapper.map_modification(self._parse_body(), resource_id)
            await ExampleCRUDService.update(resource)
            # This service only returns an HTTP 200
            self.make_response(status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

    async def delete(self, resource_id):
        try:
            if not resource_id: raise BusinessError('No resource ID specified for deletion.')
            await ExampleCRUDService.remove(resource_id)
            # This service only returns an HTTP 200
            self.make_response(status_code=200)
        except BusinessError as be:
            self.make_error_response(be.status, be.message)
        except RuntimeError:
            self.make_error_response(500, self.INTERNAL_ERROR_MESSAGE)

