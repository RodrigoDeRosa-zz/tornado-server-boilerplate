from os.path import abspath, join, dirname

from tornado.web import Application

from src.server.router import Router
from src.utils.logging.logger import Logger


class ApplicationFactory:

    @staticmethod
    def tornado_app():
        """ Create Tornado application. """
        Logger('ApplicationFactory').info('Creating Tornado Application...')
        # Define location of templates and static files
        settings = {
            'template_path': abspath(join(dirname(__file__), "../../../views/templates")),
            'static_path': abspath(join(dirname(__file__), "../../../views/static"))
        }
        # Create application by assigning routes and the location of view files
        return Application(Router.routes(), **settings)
