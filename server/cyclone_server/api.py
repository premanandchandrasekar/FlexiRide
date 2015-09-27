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
import redis

path = config.CONFIG_FILE_PATH
cfg = config.parse_config(path)
app_token = cfg['app_token']
oauth_token = cfg['oauth_token']
REDIS_HOST = "localhost"

redis_client = redis.Redis(host=REDIS_HOST)

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
        pickup_lat = self.get_argument('pickup_lat', None)
        pickup_lng = self.get_argument('pickup_lng', None)
        drop_lat = self.get_argument("drop_lat", None)
        drop_lng = self.get_argument("drop_lng", None)
        if pickup_lat and pickup_lng:
            request_url += '?pickup_lat=' + pickup_lat + '&pickup_lng=' + pickup_lng
        print request_url
        if drop_lat and drop_lng:
            request_url += '&drop_lat=' + drop_lat + '&drop_lng=' + drop_lng
        response = yield httpclient.fetch(request_url,
                       method='GET', headers=headers, postdata=None)
        print response
        print response.code
        if response.code == 200:
            jsondata = json.loads(response.body)
            success = True
        else:
            jsondata = []
            success = False
        defer.returnValue(self.write_json({'success':success, "data":jsondata}))

class CabBookingHandler(APIBase):

    @defer.inlineCallbacks
    def get(self):
        request_url = api_url + "/bookings/create"
        pickup_lat = self.get_argument('pickup_lat', None)
        pickup_lng = self.get_argument('pickup_lng', None)
        mob_no_or_pan_no = self.get_argument("user_id", None)
        sharing = self.get_argument("sharing", False)
        share_with = self.get_argument('share_with', None)
        pickup_location = self.get_argument('pickup_location', None)
        destination = self.get_argument('destination', None)
        estimated_amount = self.get_argument('estimated_amount', 200)
        share_estimated_amount = self.get_argument('share_estimated_amount', estimated_amount)        
        if not share_with:
            if pickup_lat and pickup_lng:
                request_url += '?pickup_lat=' + pickup_lat + '&pickup_lng=' + pickup_lng
            request_url += '&pickup_mode=' + 'NOW'
            response = yield httpclient.fetch(request_url,
                           method='GET', headers=headersWithAuth, postdata=None)
            print response
            if response.code == '200':
                jsondata = json.loads(response.body)
                success = True
                inserted_details = yield self.database.insert_into_bookedcabs(jsondata['driver_name'],
                    jsondata['cab_number'], jsondata['driver_number'], sharing,
                    1, estimated_amount, jsondata['eta'],jsondata['crn'])
                if inserted_details:
                    json_response = json.dumps({'details':inserted_details , 'inserted': True})
                    redis_client.publish('ridestream', json_response)
            else:
                jsondata = []
                success = False
        else:
            yield self.database.insert_into_userdetails(share_with, pickup_location,
                destination, share_estimated_amount)
            jsondata = yield self.database.fetch_bookedcabs_by_id(share_with)
            success = True
        defer.returnValue(self.write_json({'success':success, "data":jsondata}))

class BookedCabsHandler(APIBase):

    @defer.inlineCallbacks
    def get(self):
        booked_cabs = yield self.database.get_all_booked_cabs()
        print booked_cabs
        defer.returnValue(self.write_json({'success': True, 'booked_cabs_lists': booked_cabs}))

class BookedCabsCrnHandler(APIBase):

    @defer.inlineCallbacks
    def get(self):
        crn = self.get_argument('crn', None)
        booked_details_by_crn = yield self.database.get_booked_status_by_crn(crn)
        if booked_details_by_crn:
            defer.returnValue(self.write_json({'success': True, 'booked_detail': booked_details_by_crn}))
        defer.returnValue(self.write_json({'success': False}))


class LocalTest(APIBase):

    @defer.inlineCallbacks
    def get(self):
        rr = {'id': 34,
              'driver_name': 'fghgh',
              'cab_number': 'jhhjhjhj',
              'driver_mobile_number': 5555515445,
              'sharing':False,
              'device_id':99999,
              'estimated_amount':5515,
              'estimated_time':1,
              'created_on':'row.created_on',
              'crn':3699}
        json_response = json.dumps({'details':rr , 'inserted': True})
        booked_cabs = yield self.database.get_all_booked_cabs()
        redis_client.publish('ridestream', json_response)
        defer.returnValue(self.write_json({'success': True}))
