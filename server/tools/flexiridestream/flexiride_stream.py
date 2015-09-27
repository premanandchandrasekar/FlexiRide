import redis
import json
import tornado
import tornadoredis
import tornadoredis.pubsub
import sockjs.tornado
from tornado.ioloop import IOLoop
import logging
import logging.handlers
import tornado.options
import sys
import traceback
import threading
import psycopg2
from db.streaming_postgres import database
import urllib2

#import common_config
log_format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
logging.basicConfig(format=log_format, level=logging.DEBUG)
my_logger = logging.getLogger('sockjs_flexiride')
my_logger.setLevel(logging.DEBUG)
REDIS_CHAN = 'ridestream'
SOCKJS_PORT = 5001
REDIS_HOST = "localhost"

redis_client = redis.Redis(host=REDIS_HOST)
subscriber = tornadoredis.pubsub.SockJSSubscriber(tornadoredis.Client(host=REDIS_HOST))

# ---------------------------------------------------------------------------
# SockJS Tornado Stuff

def getCabsStatus():
    threading.Timer(6.0,getCabsStatus).start()
    bookedcabs = database.get_all_cabsbooked()
    print bookedcabs
    response = json.dumps({'bookedcabs_list':bookedcabs,'inserted':False })
    redis_client.publish(REDIS_CHAN,response)
    '''
    #redis_client.hincrby(HASH_NAME, 'org_count', 1)
    #count_value = redis_client.hget(HASH_NAME,'org_count')
    for k in keys:
        #count_value = "test prem"
        #k_values = randint(1,100)
        #redis_client.hincrby(HASH_NAME, k, k_values)
        count_value = redis_client.hget(HASH_NAME,k)
        response = json.dumps({k:count_value })
        #my_logger.info(response)
        print k + "S PROCESSED: " + str(count_value)
        redis_client.publish(REDIS_CHAN,response)
    for k in list_keys:
        list_value = redis_client.lrange(k, 0, 10)
        list_str = "\n".join(list_value)
        response = json.dumps({k:list_str })
        #my_logger.info(response)
        if def_val[k] != response:
            redis_client.publish(REDIS_CHAN,response)
            def_val[k] = response
            print response
    for k in unique_keys:
        redis_client.publish(REDIS_CHAN, json.dumps({k:redis_client.pfcount(k)}))
    '''
    

class FlexiRideStreamHandler(sockjs.tornado.SockJSConnection):
    client = list()

    def __init__(self, *args, **kwargs):
        super(FlexiRideStreamHandler, self).__init__(*args, **kwargs)
        subscriber.subscribe(REDIS_CHAN, self)

    def on_open(self, info):
        # Add client to the clients list
        #my_logger.debug(u'Adding client to the list')
        self.client.append(self)

    def on_message(self, message):
        #my_logger.debug(u'Sending message: {}'.format(message))
        self.send(message)

    def broadcast(self, clients, message):
        #my_logger.info(u'broadcasting message:{}'.format(message))
        i = 0
        for c in self.client:
            try:
                i += 1
                sess = c.session
                if not sess.is_closed:
                    sess.send_message(message, binary=False)
            except Exception:
                self.client.remove(c)
                my_logger.debug('Error broadcasting message for client %d - %s : %s' % (
                        i, sys.exc_info()[0], traceback.format_exc()))

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.client.remove(self)
        subscriber.unsubscribe(REDIS_CHAN, self)

ChatRouter = sockjs.tornado.SockJSRouter(FlexiRideStreamHandler, '/sockjs')

sock_app = tornado.web.Application(
        handlers=ChatRouter.urls,
        debug=True)

# ---------------------------------------------------------------------------
if __name__ == '__main__':
    getCabsStatus()
    tornado.options.parse_command_line()
    #my_logger.info('Sockjs Started')
    tornado.log.enable_pretty_logging()
    sock_app.listen(SOCKJS_PORT)
    IOLoop.instance().start()
    