from src.http_connectors.example_client_connector import ExampleClientConnector
from src.model.errors.business_error import BusinessError
from src.model.errors.example_client_error import ExampleClientError


class ExampleClientService:

    @classmethod
    async def do_request(cls):
        """ Example method to show how to call an external service. """
        try:
            client_response = await ExampleClientConnector.get_info_from_client()
        except ExampleClientError:
            raise BusinessError(f'Failed to retrieve the information from the client.')
        # Here you could do something with the response received from the client
        return client_response
