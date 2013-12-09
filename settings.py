# coding: utf-8

import logging
import os

# Только для тестирования локально

RC_IP        = os.getenv("RC_IP",        "192.168.0.1")
RC_PORT      = os.getenv("RC_PORT",      "1521")
#CURRENT_RC   = os.getenv("CURRENT_RC",   "1")
MAX_SESSIONS = 10#int(os.getenv("MAX_SESSIONS", "1"))
    
 
 
#=== ORACLE =================================================================#

# DB_SID = "ORASCLAD"
DB_SID = "FEO"


# DB_SERVERS = [  "192.168.0.1:1521", "192.168.0.161:1521", "192.168.0.170:1521", "localhost:1522"]


DB_LOGIN = "tehno"
DB_PASSWORD = "tehno"
os.environ['NLS_LANG'] = 'RUSSIAN_CIS.UTF8'


DEFAULT_CLIENT = "300020301"



FOR_TESTING = False
# FOR_TESTING = '1'


import time

TORNADO_HASH = str(time.time())

version = "3.1"
version_info = version.split('.')
server_name = 'WMS Server'


#=== OS ======================================================================#

ROOT_DIR, filename = os.path.split(os.path.abspath(__file__))


STATIC_DIR = os.path.join(ROOT_DIR, 'static')
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')

#=== SHIVA ===================================================================#
SHIVA_PORT = 12345
SHIVA_HULK_URL = "hulkexchange"
SHIVA_VERSION = '0.4.1'
SHIVA_USER_AGENT = "Shiva %s" % SHIVA_VERSION
SHIVA_LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
SHIVA_LOG_LEVEL = logging.INFO

SHIVA_LOG_FILE = ROOT_DIR + '/shiva.log'
SHIVA_LIFE_SESSION = 43200  # 12 * 60 * 60, # 12 hours in seconds
SHIVA_COOKIE_KEY = "NeZabuduMatRodnuyZXSpectrumDorogoi"
SHIVA_MAX_ALARM = 100
# каталог с картинками паспортов качества
# SHIVA_PASSPORT = "/data/image/image/"
SHIVA_PASSPORT = "/data/image/image/"

#=== AVTUK ===================================================================#
AVTUK_MAX_RECORDS = 5000


#=== Misc =========================================================================#




SUPER_USERS = 1, 4, 5
MOBILE_USER_AGENTS = ('Datalogic Memor', 
                      'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)', 
                      'Mozilla/4.0 (compatible; MSIE 6.0; Windows CE)')
