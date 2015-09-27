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

    
    def _db_error(self, err):
        print "DB ERROR : %s" % (err,)
        return None

    def _got_booked_details(self, row):
    	if row:
    		row = row[0]
    		details = {'id': row.id,
                          'driver_name': row.driver_name,
                          'cab_number': row.cab_number,
                          'driver_mobile_number': row.driver_mobile_number,
                          'sharing':row.sharing,
                          'device_id':row.device_id,
                          'estimated_amount':row.estimated_amount,
                          'estimated_time':row.estimated_time,
                          'created_on':row.created_on,
                          'crn':row.crn}
        return None


    def insert_into_bookedcabs(self, driver_name, cab_number, driver_mobile_number,
    			sharing, device_id, estimated_amount, estimated_time, crn):

        return self.connection.runOperation(
            query._INSERT_BOOKED_CAB,
            (driver_name, cab_number, driver_mobile_number,
                sharing, device_id, estimated_amount, estimated_time, crn)).\
            addCallback(self._got_booked_details).\
            addErrback(self._db_error)

    def _got_bookedcabs(self, rows):
		booked_cabs_list = []
		if rows:
			for row in rows:
				booked_cabs_list.append({'id': row.id,
                          'driver_name': row.driver_name,
                          'cab_number': row.cab_number,
                          'driver_mobile_number': row.driver_mobile_number,
                          'sharing':row.sharing,
                          'device_id':row.device_id,
                          'estimated_amount':row.estimated_amount,
                          'estimated_time':row.estimated_time,
                          'created_on':row.created_on,
                          'crn':row.crn})
		return booked_cabs_list

    def get_all_booked_cabs(self):
    	return self.connection.runQuery(
    		'SELECT * FROM cabsbooked').\
    		addCallback(self._got_bookedcabs).\
    		addErrback(self._db_error)


    def insert_into_userdetails(self, booking_id, user_mobile_number, pickup_location,
                destination, estimated_amount):
        return self.connection.runInteraction(
        	query._INSERT_INTO_USER_DETAILS, (booking_id, user_mobile_number,
        		pickup_location, destination, estimated_amount))

    def fetch_bookedcabs_by_id(self, booking_id):
    	return self.connection.runQuery(
    		query._FETCH_BOOKED_CABS_BY_ID, (booking_id)).\
    		addCallback(self.__got_booked_details).\
    		addErrback(self._db_error)

    def __got_booked_details(self, rows):
    	l = []
    	if rows:
    		for row in rows:
    			l.append({'id': row.id,
                          'driver_name': row.driver_name,
                          'cab_number': row.cab_number,
                          'driver_mobile_number': row.driver_mobile_number,
                          'sharing':row.sharing,
                          'device_id':row.device_id,
                          'estimated_amount':row.estimated_amount,
                          'estimated_time':row.estimated_time,
                          'created_on':row.created_on,
                          'crn':row.crn})
    	return l

    def get_booked_status_by_crn(self,crn):
        return self.connection.runQuery(
            query._GET_BOOKED_DETAILS_BY_CRN, (story_guid,)).\
            addCallback(self._got_booked_details).\
            addErrback(self._db_error)

    

                
    

