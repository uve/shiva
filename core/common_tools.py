# coding: utf-8

import cx_Oracle

from settings import RC_IP, RC_PORT, DB_LOGIN, DB_PASSWORD, DB_SID
#from settings import MAX_SESSIONS


from operator import itemgetter

dsn = cx_Oracle.makedsn(RC_IP, RC_PORT, DB_SID)

CLASS_NAME = "CJDEMO3"


def init_connection(self):
    
    # DB initialization
    
    try:
        self.db.ping()                
    except:
        self.pool   = Pool()
        self.db     = self.pool.acquire()        
        pass

    self.cursor = self.db.cursor()



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
        if not cls._instance:
            cls._instance = super(Pool, cls).__new__(cls, *args, **kwargs)        
            cls.pool = cx_Oracle.SessionPool(user=DB_LOGIN, password=DB_PASSWORD, dsn=dsn, min=1, max=4, increment=1, threaded=True)
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


    '''Взять из базы одну запись, извлечь названия всех колонок и вернуть словарь'''    
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