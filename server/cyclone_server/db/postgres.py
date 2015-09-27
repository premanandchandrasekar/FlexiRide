from twisted.internet import defer
import query
from datetime import datetime
import psycopg2
from cyclone_server.db import cache
from twisted.python import log
from collections import defaultdict



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
    
    def _db_error(self, err):
        print "DB ERROR : %s" % (err,)
        return None

    def _got_bookedcabs(self, rows):
		bookes_cabs_list = []
		if rows:
			for row in rows:
				bookes_cabs_list.append({'id': row.id,
                          'driver_name': row.driver_name,
                          'cab_number': row.cab_number,
                          'driver_mobile_number': row.driver_mobile_number,
                          'sharing':row.sharing,
                          'device_id':row.device_id,
                          'estimated_amount':row.estimated_amount,
                          'estimated_time':row.estimated_time,
                          'created_on':row.created_on,
                          'crn':row.crn})
		return bookes_cabs_list

    def get_all_booked_cabs(self):
    	return self.connection.runQuery(
    		'SELECT * FROM cabsbooked').\
    		addCallback(self._got_bookedcabs).\
    		addErrback(self._db_error)

    

                
    

