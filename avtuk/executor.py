# coding: utf-8

__all__ = ("Executor", "gatekeeper",)

from hashlib import md5
import re
from time import time
from avtuk.swcls import SWCLS
from avtuk.multiobj import AvtukMultiObject

from core.common_tools import init_connection, close_connection


# import cx_Oracle

#==============================================================================
class SingletonMeta(type):
    def __init__(cls, name, bases, kw):
        super(SingletonMeta, cls).__init__(name, bases, kw)
        cls.instance = None
    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = super(SingletonMeta, self).__call__(*args, **kw)
        return self.instance


#==============================================================================
class AvtukExecutor(object):
    '''Поддерживаются: oracle, sqlite3'''
    __metaclass__ = SingletonMeta


    def __init__(self):
        
                
        
        self.default_database = ''
        self.max_record = 5000
        
        # { class_name : cls }
        self.classes = {}
        
        # {ALIAS: [connect(), lambda, type_db,]}
        self.connects = {}

        # {MD : (OBJ, LIV, [tables,], SQL[:100])}
        self._obj_cash = {}
        
        

        # regex для поиска имен таблиц убираемых из кэша
        # self._re_tbl = re.compile(ur"(?i)\bupdate\s+(\S+)\b|\binsert\s+(?:\binto\b)?\s+(\S+)\b|\btruncate\s+table\s+(\S+)\b|\bdelete\s+(?:\bfrom\b)?\s+(\S+)\b", re.M | re.S | re.U)
        self._re_tbl = re.compile("(?i)\bupdate\s+(\S+)\b|\binsert\s+(?:\binto\b)?\s+(\S+)\b|\btruncate\s+table\s+(\S+)\b|\bdelete\s+(?:\bfrom\b)?\s+(\S+)\b", re.M | re.S | re.U)

    def __repr__(self):
        return '<AvtukExecutor aliases:%s, ch:%s>' % (self.connects.keys(), self._obj_cash.keys())



    def vacuum(self, tbl=set()):
        ''' clear old data '''
        t = int(time())
        for i in [k for k, v in self._obj_cash.items() if v[1] < t or v[2] & tbl]:
            del self._obj_cash[i]



    def exec_sql(self, sql, **kw):
        
   
        alias = kw.pop('alias', None)
        alias = alias #For no warnings
        multi = kw.pop('multi', None)
        
 
        # DB initialization
        init_connection(self)
         
        self.execute(sql, **kw)
        self.db.commit()
              
        
        # удаление из кэша если INSERT, DELETE, UPDATE, TRUNCATE
        tbl = set()
        for i in self._re_tbl.finditer(sql):
            tbl.update(j for j in i.groups() if j)
        if tbl:
            self.vacuum(tbl)


        ret = dict(count=0, fields=[], data=[])

        if not multi is None:
            ret['data'] = (self.cursor.fetchall()[:self.max_record] if multi else self.cursor.fetchone()) or []
            ret['count'] = self.cursor.rowcount
            
            ret['fields'] = [i[0].lower() for i in self.cursor.description]
            
        close_connection(self)

        return ret


    def exec_cls(self, sql, **kw):
        kw.setdefault('multi', True)
        # kw.setdefault('alias', self.default_database)

        live = kw.pop('live', 0)
        cls_1 = kw.pop('cls', SWCLS)
        cls_2 = AvtukMultiObject if kw['multi'] else cls_1

        md = md5(sql + ':' + str(sorted(kw.items()))).hexdigest()
        self.vacuum()

        '''
        if md in self._obj_cash:
            #print 'CAS', cls, sql[:15]
            return self._obj_cash[md][0]
        '''
        try: 
            
            data = self.exec_sql(sql, **kw)
            res = cls_2(md, cls=cls_1, **data)
        except: 
            res = None
        

        if live:
            tbl = cls_1.__dict__.get('__table__', None)
            # tbl = [tbl] if tbl else [i.group(1) for i in re.finditer(ur"(?i)from\s+(\w+)", sql)]
            tbl = [tbl] if tbl else [i.group(1) for i in re.finditer("(?i)from\s+(\w+)", sql)]

            self._obj_cash[md] = [res, int(time()) + live, set(tbl), sql[:100]]

        return res


    def kill(self, uin):
        if uin in self._obj_cash:
            del self._obj_cash[uin]


    def save(self, sql, **kw):
        ''' Для SQL = INSERT, UPDATE, DELETE и пр. '''
        # self.vacuum()
        self.kill(kw.pop('uin', None))

        return  self.exec_sql(sql, **kw)


#==============================================================================
Executor = AvtukExecutor()

