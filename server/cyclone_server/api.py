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
from cyclone_server import httpclient

path = config.CONFIG_FILE_PATH
cfg = config.parse_config(path)
app_token = cfg['app_token']
oauth_token = cfg['oauth_token']


api_url = cfg['api_url']

headers = {"X-APP-Token": [app_token]}

headersWithAuth = {"X-APP-Token": [app_token],
                   "Authorization": ["Basic %s" % (oauth_token)]}


class APIBase(BaseHandler, DatabaseMixin):
    no_xsrf = True

    def get_config(self):
        path = config.CONFIG_FILE_PATH
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


class FetchAvailableCabs(APIBase):
    
    @defer.inlineCallbacks
    def get(self):
        request_url = api_url + "/products"
        pickup_lat = self.get_argument('pickup_lat')
        pickup_lng = self.get_argument('pickup_lng')
        request_url += '?pickup_lat=' + pickup_lat + '&pickup_lng=' + pickup_lng
        print request_url
        response = yield httpclient.fetch(request_url,
                       method='GET', headers=headers, postdata=None)
        print response
        jsondata = json.loads(response.body)
        print jsondata
        success = True
        defer.returnValue(self.write_json({'success':success, "data":jsondata}))


