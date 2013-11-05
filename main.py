  #!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging

import settings as config
from core.sessions import Sessions


import tornado.web
import tornado.httpserver                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
from tornado.ioloop import IOLoop

import urls 

from settings import RC_IP, RC_PORT

from tornado.web import Application


from settings import MAX_SESSIONS


#=============================================================================#
class MissingHandler(tornado.web.RequestHandler):
    def get(self, path):
        logging.warning('Invalid GET: %s' % path)
        raise tornado.web.HTTPError(404)

    def post(self, path):
        logging.warning('Invalid POST: %s' % path)
        self.write("{error:404}")

#=============================================================================#
if __name__ == "__main__":
    

    logging.basicConfig(format=config.SHIVA_LOG_FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        # filename=config.SHIVA_LOG_FILE,
                        level=config.SHIVA_LOG_LEVEL)
 

    logging.info('      |   _)')
    logging.info(' (_-<   \  |\ \ / _` |')
    logging.info(' ___/_| _|_| \_/\__,_|')
    logging.info('"%s"' % config.SHIVA_USER_AGENT)
    logging.info('Tornado version: %s' % tornado.version)
    logging.info('CURRENT RC: %s' % (config.CURRENT_RC))
    logging.info('WMS Server started [port %s]' % (config.SHIVA_PORT))
    
    logging.info('Oracle connection: %s:%s' % (RC_IP, RC_PORT))
    
    
    app = Application(handlers=urls.handlers, **{
            'static_path': config.STATIC_DIR,
            'default_handler':MissingHandler,
            'debug': False,
            'gzip' : True
        })


    app.sessions = Sessions()
    # кэш имен файлов паспортов качества - {'имя':None} 33
    app.passport_cash = {}


    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    #http_server.listen(config.SHIVA_PORT)
        
    
    http_server.bind(config.SHIVA_PORT)
    #loop = tornado.ioloop.IOLoop.instance()

    http_server.start(MAX_SESSIONS)  # autodetect number of cores and fork a process for each
    IOLoop.instance().start()
