from twisted.internet import defer
import query
from datetime import datetime
import psycopg2



class PostgresDatabase(object):
    def __init__(self, connection, cache=None):
        self.connection = connection
        self.cache = cache

    def insert_into_bookedcabs(self, driver_name, cab_number, driver_mobile_number,
    			sharing, device_id, estimated_amount, estimated_time):

        return self.connection.runInteraction(
            query._INSERT_BOOKED_CAB,
            (driver_name, cab_number, driver_mobile_number,
                sharing, device_id, estimated_amount, estimated_time))

    

                
    

