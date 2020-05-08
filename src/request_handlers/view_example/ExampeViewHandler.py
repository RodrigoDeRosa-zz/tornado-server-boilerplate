from tornado.template import Loader

from src.request_handlers.custom_request_handler import CustomRequestHandler


class ExampleViewHandler(CustomRequestHandler):
    """ Example handler that renders an HTML view. """

    SUPPORTED_METHODS = ['GET']

    def get(self):
        loader = Loader(self.get_template_path())
        self.write(loader.load('home.html').generate(static_url=self.static_url))
