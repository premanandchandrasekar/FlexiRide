from twisted.internet import reactor

from txmongo._pymongo.objectid import ObjectId

from .objects import User
class MongoDatabase(object):
    def __init__(self, connection, cache):
        self.connection = connection
        self.cache = cache
