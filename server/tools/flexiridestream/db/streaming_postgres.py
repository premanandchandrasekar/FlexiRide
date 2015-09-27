import psycopg2
import sys
import datetime
import json
import urllib
from contextlib import closing
from psycopg2 import extras
from collections import defaultdict
from datetime import date


#Database connection#################################################################################
#db_conn = app.config['DB_CONN']
db_conn = "dbname=flexiride user=foo password=bar host=localhost port=5432"


class database:

    @classmethod
    def _get_cursor(cls, connection):
        return closing(connection.cursor())

    @classmethod
    def _get_dict_cursor(cls, connection):
        return closing(connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor))

    @classmethod
    def __getCursor(cls, connection, dct):
        if dct:                 
            return cls._get_dict_cursor(connection)
        else:
            return cls._get_cursor(connection)

    @classmethod
    def _get_connection(cls):
        return closing(psycopg2.connect(db_conn))

    @classmethod
    def __fetchOne(cls, query, params, dct=False):
        with cls._get_connection() as connect:
            with cls.__getCursor(connect, dct) as curs:
                curs.execute(query, params)
                row = curs.fetchone()
        if row:
            return row
        return None

    @classmethod
    def __fetchAll(cls, query, params, dct=False):
        with cls._get_connection() as connect:
            with cls.__getCursor(connect, dct) as curs:
                curs.execute(query, params)
                rows = curs.fetchall()
        if rows:
            return rows
        return None

    @classmethod
    def __insert(cls, query, params, dct=False):
        with cls._get_connection() as connect:
            with cls.__getCursor(connect, dct) as curs:
                curs.execute(query, params)
                connect.commit()

    @classmethod
    def __insertAndFetch(cls, query, params, dct=False):
        with cls._get_connection() as connect:
            with cls.__getCursor(connect, dct) as curs:
                curs.execute(query, params)
                connect.commit()
                row = curs.fetchone()
        if row:
            return row
        return None

    @classmethod
    def __update(cls, query, params, dct=False):
        with cls._get_connection() as connect:
            with cls.__getCursor(connect, dct) as curs:
                curs.execute(query, params)
                connect.commit()

    @classmethod
    def __updateAndFetch(cls, query, params, dct=False):
        with cls._get_connection() as connect:
            with cls.__getCursor(connect, dct) as curs:
                curs.execute(query, params)
                connect.commit()
                row = curs.fetchone()
        if row:
            return row
        return None

    @classmethod
    def __delete(cls, query, params, dct=False):
        with cls._get_connection() as connect:
            with cls.__getCursor(connect, dct) as curs:
                curs.execute(query, params)
                connect.commit()

    @classmethod
    def get_all_cabsbooked(cls):
        query = "SELECT * FROM cabsbooked"
        subscriber_data = cls.__fetchAll(query,'')
        if subscriber_data:
            bookes_cabs_list = []
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
            return subscriber_data
        return bookes_cabs_list
