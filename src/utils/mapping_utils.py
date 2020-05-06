import ast


class MappingUtils:

    @staticmethod
    def decode_request_body(body: bytes) -> dict:
        """ Remove unwanted characters from the given body. """
        return ast.literal_eval(body.decode('utf-8').replace('\t', '').replace('\n', ''))
