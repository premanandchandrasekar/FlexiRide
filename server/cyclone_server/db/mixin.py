from twisted.internet import defer

from cyclone_server.db.postgres import PostgresDatabase
from psycopg2.extras import NamedTupleConnection

from twisted.enterprise.adbapi import ConnectionPool




DB_WRAPPER_MAP = {
        #'mongodb': (MongoDatabase, '_connect_mongo'),
        'postgresql': (PostgresDatabase, '_connect_postgres')
}

redis_connection_settings = None
postgres_connection_settings = None


class DatabaseMixin(object):
    redis = None
    mongodb = None
    postgresql = None

    @classmethod
    def setup(cls, settings, sync=False):
        cls.redis_cache = None
        conf = settings.get("redis_settings")
                
        conf = settings.get("postgresql_settings")
        if conf:
            postgres_connection_settings = dict(
                    host=conf.host, port=conf.port,
                    database=conf.database, user=conf.username,
                    password=conf.password,
                    cp_min=1, cp_max=conf.poolsize,
                    cp_reconnect=True, cp_noisy=settings['debug'],
                    connection_factory=NamedTupleConnection)
            pg_cpool = ConnectionPool("psycopg2",
                    **postgres_connection_settings)
            cls.postgresql = pg_cpool
            print pg_cpool

        cls.preferred_db_class = DB_WRAPPER_MAP['postgresql'][0]
        cls._connect = getattr(cls, DB_WRAPPER_MAP['postgresql'][1])

      
    def _connect_postgres(self):
        return self.postgresql

    def _connect_mongo(self):
        connection = getattr(self.mongodb,
                self.settings['mongodb_settings'].database)
        return connection

    @property
    def database(self):
        if not hasattr(self, '_db'):
            connection = self._connect()
            self._db = self.preferred_db_class(connection, self.redis_cache)
        return self._db
