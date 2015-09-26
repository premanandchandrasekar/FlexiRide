import cyclone.locale
import cyclone.web

from cyclone_server.db.mixin import DatabaseMixin
from cyclone_server import routes

class Application(cyclone.web.Application):
    def __init__(self, settings):
        handlers = routes.routes

        # Initialize locales
        locales = settings.get("locale_path")
        if locales:
            cyclone.locale.load_gettext_translations(locales, "cyclone_server")

        # Set up database connections
        DatabaseMixin.setup(settings)

        cyclone.web.Application.__init__(self, handlers, **settings)
