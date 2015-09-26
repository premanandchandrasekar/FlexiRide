import re
import functools
import cyclone.web
from twisted.python import log
from cyclone_server import config


class MongoDocWrapper(object):
    def __init__(self, d):
        self.d = d

    def __getattr__(self, name):
        if name == '_id':
            return str(self.d[name])
        return self.d[name]


class BaseHandler(cyclone.web.RequestHandler):
    is_login_handler = False
    is_index_handler = False

    def send_error(self, status_code=500, **kwargs):
        try:
            #collect exception details
            emsg = None
            r_host = None
            r_uri = None
            r_user_agent = None

            if "exc_info" in kwargs:
                e = kwargs["exc_info"][1]

                if e:
                    emsg = str(e)

            elif "exception" in kwargs:
                e = kwargs["exception"]
                emsg = str(e)

            log.msg('send_error: EXCEPTION : %s' % (emsg))

            r_host = self.request.host
            r_uri = self.request.uri
            r_user_agent = self.request.headers['User-Agent']
            r_client_ip = self.get_remote_ip()

        except Exception as ex:
            log.msg('status code : %s, Exception in send_error: %s' % (status_code, str(ex)))

        #call base method
        super(BaseHandler, self).send_error(status_code, **kwargs)

        
    def get_remote_ip(self):
            #remote_ip will be proxy ip (127.0.0.1) in the server as we are behind
            #nginx and varnish. Use X-Forwarded-For which will set to original client ip
            #r_remote_ip =self.request.remote_ip
            r_client_ip = None
            if 'X-Forwarded-For' in self.request.headers:
                r_client_ip = self.request.headers['X-Forwarded-For']
            else:
                r_client_ip = self.request.remote_ip
            return r_client_ip


class TornadoMultiDict(object):
    def __init__(self, handler):
        self.handler = handler

    def __iter__(self):
        return iter(self.handler.request.arguments)

    def __len__(self):
        return len(self.handler.request.arguments)

    def __contains__(self, name):
        # We use request.arguments because get_arguments always returns a
        # value regardless of the existence of the key.
        return (name in self.handler.request.arguments)

    def getlist(self, name):
        # get_arguments by default strips whitespace from the input data,
        # so we pass strip=False to stop that in case we need to validate
        # on whitespace.
        return self.handler.get_arguments(name, strip=False)


def get_config():
    path = config.config_file_path()
    settings = config.parse_config(path)
    return settings



