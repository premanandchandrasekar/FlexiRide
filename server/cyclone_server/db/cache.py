import cPickle as pickle
from twisted.internet import defer
import json
expiry = 7200

serialized_suffix = '-ser'


class BaseCache(object):
    _cache = dict()
    _serializer = pickle

    def _serial(self, obj):
        return self._serializer.dumps(obj)

    def _unserial(self, string):
        return self._serializer.loads(str(string))

    def __contains__(self, item):
        """
        :param item: Key
        :rtype: bool
        """
        raise NotImplementedError(
            "def __contains__ -- %s" % self.__class__.__name__)

    def __getitem__(self, key):
        """
        :param str key: key name
        :rtype: list
        """
        raise NotImplementedError(
            "def __getitem__ -- %s" % self.__class__.__name__)

    def __setitem__(self, key, message):
        """
        :param str key: key name
        :param list message: value
        """
        raise NotImplementedError(
            "def __setitem__ -- %s" % self.__class__.__name__)

    def keylen(self, key):
        """
        :param str key: key name
        :rtype: int
        """
        raise NotImplementedError("def keylen -- %s" % self.__class__.__name__)

    def extend(self, key, message):
        """
        :param str key: key name
        :param list message: value
        """
        raise NotImplementedError("def extend -- %s" % self.__class__.__name__)


class RedisCache(BaseCache):
    def __init__(self, conf):
        from cyclone import redis as cyredis
        conn = cyredis.ConnectionPool(
            conf.host, conf.port, conf.dbid, conf.poolsize)
        conn.addCallback(lambda c: setattr(
            self, '_cache', c))

    def contains(self, item, serialized=False):
        if serialized:
            item += serialized_suffix
        return self._cache.exists(item)

    def delete(self, key, serialized=False):
        if serialized:
            key += serialized_suffix
        print 'Deleting Cache Key ' + key
        if self._cache.exists(key):
            self._cache.delete(key)

    def __contains__(self, item):
        return self._cache.exists(item)

    def _got_item(self, item, serialized=False):
        if item:
            if serialized:
                return json.loads(item)
            else:
                return self._unserial(item)
        return None

    def __getitem__(self, key):
        return self._cache.hget(
            key, 'data').addCallback(self._got_item, False)

    @defer.inlineCallbacks
    def __setitem__(self, key, message):
        if self._cache.exists(key):
            yield self._cache.delete(key)
        self.extend(key, message)

    @defer.inlineCallbacks
    def set_serialized(self, key, obj_dict):
        key += serialized_suffix
        if self._cache.exists(key):
            yield self._cache.delete(key)
        self.extend(key, obj_dict, True)

    def get_serialized(self, key):
        key += serialized_suffix
        return self._cache.hget(
            key, 'data').addCallback(self._got_item, serialized=True)

    def keylen(self, key):
        return self._cache.llen(key)

    @defer.inlineCallbacks
    def extend(self, key, message, serialized=False):
        if serialized:
            yield self._cache.hset(key, 'data', json.dumps(message))
        else:
            yield self._cache.hset(key, 'data', self._serial(message))
        self._cache.expire(key, expiry)

    def __delitem__(self, key):
        return self._cache.delete(key)

    def invalidate(self, key):
        return self._cache.delete(key)