# coding: utf-8

import hashlib, os
from core.common_tools import init_connection, close_connection

from tornado.web import RequestHandler
from tornado.httpclient import HTTPError

from tornado.escape import json_encode, json_decode




from core.sessions import SessionManager#Session, uid2sid

from settings import TORNADO_HASH, STATIC_DIR

from core.utils import Storage
import logging
import cx_Oracle

from tornado.log import app_log, gen_log
from tornado import httputil
import sys
#=============================================================================#
ICO_DIR = os.path.join(STATIC_DIR, 'ico_bar')



#=============================================================================#
class BaseHandler(RequestHandler):
    urls = []

    def initialize(self):
        
        
        self.set_header("tornado_hash", TORNADO_HASH)
        self.set_header("Cache-control", "public")
        
        # DB initialization
        init_connection(self)                
        
        uid  = self.get_cookie('uid')
        role = self.get_cookie('role')
        rc   = self.get_cookie('rc')
        self.session = SessionManager(uid, role, rc)


    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', '*')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Max-Age', 604800)
        self.set_header('Access-Control-Allow-Headers', '*')
        
       
        

    def on_finish(self):
        """Called after the end of a request.

        Override this method to perform cleanup, logging, etc.
        This method is a counterpart to `prepare`.  ``on_finish`` may
        not produce any output, as it is called after the response
        has been sent to the client.
        """            
        
        close_connection(self)   


    
    
    def _handle_request_exception(self, e):
        
        close_connection(self)
                
        if isinstance(e, HTTPError):
            if e.log_message:
                error_format = "%d %s: " + e.log_message
                args = [e.status_code, self._request_summary()] + list(e.args)
                gen_log.warning(error_format, *args)
            if e.status_code not in httputil.responses and not e.reason:
                gen_log.error("Bad HTTP status code: %d", e.status_code)
                self.send_error(500, exc_info=sys.exc_info())
            else:
                self.send_error(e.status_code, exc_info=sys.exc_info())

        elif isinstance(e, NameError):
            app_log.error("Uncaught exception %s\n%r", self._request_summary(),
                          self.request, exc_info=True)
            self.send_error(500, exc_info=sys.exc_info())


                       
        elif isinstance(e, cx_Oracle.DatabaseError):

            #msg = re.sub('str:|PL/SQL|на"TEHNO.\d+"|на "TEHNO.SHIVA_TASK"| на"TEHNO.SHIVA", на| , на|ORA-\d+|:|\\n|line \d+|  +', "", msg)

            try:
                msg = e.message.message
            except:
                msg = e.message

            text = msg.split("%%")
            if len(text) > 2:
                msg = text[1]
            
            self.write({'error': msg })
            self.finish()            
                            
        else:
            app_log.error("Uncaught exception %s\n%r", self._request_summary(),
                          self.request, exc_info=True)
            self.send_error(500, exc_info=sys.exc_info())
            
        
        
    
    
    def write_XML(self, xml):
        if not self._write_buffer:
            self.set_header("Content-Type", "text/xml; charset=utf-8")
            self.write('<?xml version="1.0" encoding="UTF-8"?>')
        self.write(xml)


    def write(self, chunk):
        """Writes the given chunk to the output buffer.

        To write the output to the network, use the flush() method below.

        If the given chunk is a dictionary, we write it as JSON and set
        the Content-Type of the response to be text/javascript.

        Note that lists are not converted to JSON because of a potential
        cross-site security vulnerability.  All JSON output should be
        wrapped in a dictionary.  More details at
        http://haacked.com/archive/2008/11/20/anatomy-of-a-subtle-json-vulnerability.aspx
        """
        # if isinstance(chunk, dict):
        # if isinstance(chunk, (tuple, dict)):
        if isinstance(chunk, (list, tuple, dict)):
            chunk = json_encode(chunk)
            self.set_header("Content-Type", "application/json; charset=utf-8")
        chunk = _utf8(chunk)

        if chunk is not None:
            self._write_buffer.append(chunk)


    def input(self, **defaults):
        mas = self.request.arguments
        if isinstance(mas, dict):

            try:
                if mas:
                    for i, v in mas.items():
                        if not isinstance(v, str) and not isinstance(v, int) and not isinstance(v, float):
                            mas[i] = v[0]
                else:
                    logging.info(self.request.body)
                    mas = json_decode(self.request.body)
                    
                defaults.update(mas)
            except:
                pass
        
        return Storage(defaults)

    def input_list(self, **defaults):
        if isinstance(self.request.arguments, dict):
            defaults.update(self.request.arguments)

        return Storage(defaults)


def _utf8(s):
    if isinstance(s, unicode):
        return s.encode("utf-8")
    # assert isinstance(s, str)
    return s


def _unicode(s):
    if isinstance(s, str):
        try:
            return s.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPError(400, "Non-utf8 argument")
    # assert isinstance(s, unicode)
    return s


#=============================================================================#

class UserError(HTTPError): 
    def __init__(self, status_code, user_message, log_message=None, *args):
        HTTPError.__init__(self, status_code, log_message, *args) 
        self.user_message = user_message 

    def get_error_html(self, status_code, **kwargs): 
        e = kwargs.get("exception") 
        if e and isinstance(e, UserError): 
            return e.user_message 


#=============================================================================#
def md5passw(login, passw): return hashlib.md5('%s SHIVA %s' % (passw, login)).hexdigest()

#=============================================================================#
def escape(*args):
    return tuple([i.replace("&", "&amp;").\
                  replace("<", "&lt;").\
                  replace(">", "&gt;").\
                  replace('"', "&quot;").\
                  replace("'", "&apos;") for i in args])

#=============================================================================#
def get_icons(full_path=True):
    ext = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
    x = [full_path and '/static/ico_bar/%s' % i or i for i in os.listdir(ICO_DIR) if os.path.splitext(i)[-1][1:].lower() in ext]
    x.sort()
    return x


#==============================================================================
if __name__ == "__main__":
    pass
