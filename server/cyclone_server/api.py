import json
from twisted.python import log

import cyclone
from cyclone_server.db import mixin
from cyclone_server import utils 
from cyclone_server.utils import BaseHandler
from cyclone_server.db.mixin import DatabaseMixin
from cyclone_server import config
from twisted.internet import defer
from image_processor import ImageProcessor


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


class CamUploadHandler(APIBase):

    def post(self):
        datafile = self.request.files['webcam'][0]

        image = ImageProcessor(datafile['body'])
        image.process()
        
        return self.write_json({'success': True,
                                'text': image.text,
                                'pan_no': image.pan_no
        })