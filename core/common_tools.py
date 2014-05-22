# coding: utf-8

import cx_Oracle

from settings import RC_IP, RC_PORT, DB_LOGIN, DB_PASSWORD, DB_SID, MAX_SESSIONS
#from settings import MAX_SESSIONS

import logging

from operator import itemgetter

dsn = cx_Oracle.makedsn(RC_IP, RC_PORT, DB_SID)

CLASS_NAME = "CJDEMO3"

def callproc(self, args, kwargs):    
    
    params = ", ".join([str(k) for k in args[1:]])
    logging.info("Call Proc: %s \tparams: %s", args[0], params)
    
    self.cursor.callproc('shiva.exec_log', [args[0], params, self.session.uid])
    
    return self.cursor.callproc(*args, **kwargs)
    
    
    
def callfunc(self, args, kwargs):    
        
    params = ", ".join([str(k) for k in args[1:]])
    logging.info("Call Func: %s \tparams: %s", args[0], params)
    
    self.cursor.callproc('shiva.exec_log', [args[0], params, self.session.uid])

    return self.cursor.callfunc(*args, **kwargs)    
    
    
    
def callexec(self, args, kwargs):    
    
    #logging.info("Call Execute: %s \tparams: %s", args[0], args[1:])
    return self.cursor.execute(*args, **kwargs)       



def init_connection(self):
    
    # DB initialization
    
    try:
        self.db.ping()                
    except:
        self.pool   = Pool()
        self.db     = self.pool.acquire()
        self.db.autocommit = True

        pass



    self.cursor = self.db.cursor()
       
    self.proc    = lambda *a, **k: callproc(self, a, k)
    self.func    = lambda *a, **k: callfunc(self, a, k)
    self.execute = lambda *a, **k: callexec(self, a, k)
    


def close_connection(self):
    
    # DB close    
    try:
        self.db.commit()
        self.cursor.close()           
        self.pool.release(self.db)
    except:
        pass  



class Pool(object):
    
    _instance = None
        
    def __new__(cls, *args, **kwargs):
        if not cls._instance or not cls.pool:
            cls._instance = super(Pool, cls).__new__(cls, *args, **kwargs)        
            cls.pool = cx_Oracle.SessionPool(user=DB_LOGIN, password=DB_PASSWORD, dsn=dsn, min=1, max=MAX_SESSIONS*2, increment=1, threaded=True)
            cls.pool.timeout = 300
        
        return cls.pool
    
    
    
    '''Взять из базы одну запись, извлечь названия всех колонок и вернуть словарь'''    
def fetchone(item):

    values = item.fetchone() 
    
    if not values:
        return None
    
    colums = map(itemgetter(0), item.description)            
    colums = map(lambda x: x.lower(), colums)
     
    result = dict(zip(colums, values))
    
    return result


    '''Взять из базы все записи, извлечь названия всех колонок и вернуть словарь'''    
def fetchall_by_name(item):

    results = []
    
    colums = map(itemgetter(0), item.description)            
    colums = map(lambda x: x.lower(), colums)
     
    for item in item.fetchall():
        results.append( dict(zip(colums, item)) )
    
    return results




    '''Взять из базы все записи, и преобразовать к формату dHTMLXgrid json'''
def fetchall(item=None, count=0):

    data = item.fetchall()    
    results = []
     
    for item in data:            
        results.append({"id": item[count], "data": item })

    return {"rows": results} 