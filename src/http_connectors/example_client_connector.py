from json import loads

from src.http_connectors.generic_http_connector import GenericHTTPConnector
from src.model.errors.example_client_error import ExampleClientError
from src.model.errors.http_connector_error import HTTPConnectorError
from src.utils.annotations.retry_coroutine import retry_coroutine


class ExampleClientConnector(GenericHTTPConnector):

    @classmethod
    @retry_coroutine(ExampleClientError, attempts=5, delay=0.5)  # The request will be tried 5 times
    async def get_info_from_client(cls):
        """ Retrieve event from Lookout. """
        try:
            cls.get_logger().info('Doing request to external service.')
            response = await cls.do_async_request('http://localhost:8573/anExample?aQuery=param')
        except HTTPConnectorError as hce:
            raise ExampleClientError(hce.message)
        # Response mapping should be done here if you wanted to transform from JSON to application model
        return loads(response.body)
