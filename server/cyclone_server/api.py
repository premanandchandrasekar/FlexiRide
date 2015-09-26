import json
from twisted.python import log

import cyclone
from cyclone_server.db import mixin
from cyclone_server import utils 
from cyclone_server.utils import BaseHandler
from cyclone_server.db.mixin import DatabaseMixin
from cyclone_server import config
from twisted.internet import defer


class APIBase(BaseHandler, DatabaseMixin):
    no_xsrf = True

    def get_config(self):
        path = config.config_file_path()
        settings = config.parse_config(path)
        return settings

    def prepare(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")

    def write_json(self, d):
        self.set_header("Content-Type", "application/json")
        return self.write(json.dumps(d, sort_keys=True, indent=4))


class DetailsHandler(APIBase):

    def get(self):
        return self.write_json({'success': True, 'data': response})

