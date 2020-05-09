from tornado.httpclient import AsyncHTTPClient, HTTPError, HTTPRequest

from src.model.errors.http_connector_error import HTTPConnectorError
from src.utils.logging.logger import Logger


class GenericHTTPConnector:

    AsyncHTTPClient.configure(None, max_clients=1000)

    @classmethod
    async def do_async_request(cls, url, method='GET', headers=None, body=None, timeout=None, verify=True):
        """ Make request with tornado's asynchronous AsyncHTTPClient. """
        client = AsyncHTTPClient()
        request = cls.__create_request(url, method, headers, body, timeout, verify)
        try:
            return await client.fetch(request)
        except HTTPError as he:
            raise HTTPConnectorError(he.message)
        except Exception as e:
            raise HTTPConnectorError(e)
        finally:
            client.close()

    @staticmethod
    def __create_request(url, method, headers, body, timeout, verify):
        return HTTPRequest(
            url=url,
            method=method,
            headers=headers,
            body=body,
            request_timeout=timeout,
            validate_cert=verify
        )

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
