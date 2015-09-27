import re
import cyclone.web
from cyclone_server.db.postgres import PostgresDatabase
from twisted.internet import defer
from cyclone_server import utils
from cyclone_server.utils import BaseHandler
from cyclone_server.db.mixin import DatabaseMixin
from cyclone_server.api import CabBookingHandler

class IndexHandler(BaseHandler, DatabaseMixin):
    is_index_handler = True

    def get(self):
        #db = PostgresDatabase(self)
        #Merchant_lists = yield self.database.get_list_of_merchant()
        self.render("index.html")


class SampleWebcamHandler(cyclone.web.RequestHandler):

    def get(self):
        self.render("webcam.html")

class ShowBookedCabsDetails(cyclone.web.RequestHandler):

    def get(self):
        self.render("booked_cabs_details.html")

class ShowConfirmationHandler(cyclone.web.RequestHandler):

    def get(self, crn_id):
        self.render("confirmation.html",crn_id=crn_id)
