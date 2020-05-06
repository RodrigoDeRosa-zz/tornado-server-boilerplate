from src.model.errors.business_error import BusinessError
from src.model.example_resource import ExampleResource


class ExampleRequestMapper:

    @staticmethod
    def map_creation(request_body: dict) -> ExampleResource:
        # Create model object
        return ExampleResource(
            id=request_body['id'],
            name=request_body['name'],
            value=request_body['value'],
        )

    @staticmethod
    def map_modification(request_body: dict, resource_id: str) -> ExampleResource:
        # Check if the request contains all needed fields
        if not resource_id: raise BusinessError('Resource ID is compulsory for this service.', 400)
        if not request_body: raise BusinessError('Tried to update doctor with an empty patch body.', 400)
        # Create model object only with the elements that were received
        resource = ExampleResource(id=resource_id)
        if 'name' in request_body: resource.name = request_body['name']
        if 'value' in request_body: resource.value = request_body['value']
        return resource
