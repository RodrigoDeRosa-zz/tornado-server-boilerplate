from gzip import compress


class GzipUtils:

    @classmethod
    def accepts_gzip_compression(cls, headers) -> bool:
        """ Checks if Accept-Encoding: gzip is present in given headers. """
        return 'Accept-Encoding' in headers and 'gzip' in headers['Accept-Encoding']

    @classmethod
    def gzip_compress(cls, data: str) -> bytes:
        """ Receives a string and returns its binary representation, compressed with GZIP. """
        return compress(bytes(data, 'utf-8'))
