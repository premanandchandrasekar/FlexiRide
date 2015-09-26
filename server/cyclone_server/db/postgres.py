from twisted.internet import defer
import query
from datetime import datetime
import psycopg2



class PostgresDatabase(object):
    def __init__(self, connection, cache=None):
        self.connection = connection
        self.cache = cache

    

                
    

