# coding: utf-8

__all__ = ('AvtukObject', 'Sequence',)

# import types
import re
from types import FunctionType, MethodType, BuiltinFunctionType, BuiltinMethodType
from tokenize import generate_tokens

from columns import CustomCol, Reference
from executor import Executor
from tools import jsDict
from render import DHTMLX_Render

#============================================================================#
class Sequence(object):
    def __init__(self, sec, alias=''):
        self.sec = sec
        self.alias = alias

    def __call__(self):
        sql = "SELECT %s.nextval FROM dual" % self.sec
        return Executor.exec_sql(sql, multi=False, alias=self.alias)['data'][0]


#==============================================================================
class AvtukMetaObject(type):
    def __new__(cls, class_name, bases, new_attrs):
        # print 'META0:', class_name

        cls = type.__new__(cls, class_name, bases, new_attrs)
        if class_name == 'AvtukObject': return cls

        if class_name not in Executor.classes:
            Executor.classes[class_name] = cls

        cls._fields = jsDict()  # все поля { property : Col() }
        cls._pk = []  # список PK (id)
        cls._basic_fields = {}  # property:db_field
        cls._basic_sdleif = {}  # db_field:property        
        cls._reference_fields = []  # список внешних полей

        for k, v in new_attrs.items():
            if isinstance(v, CustomCol):
                delattr(cls, k)

                if isinstance(v, (Reference)):
                    cls._reference_fields.append(k)
                else:
                    if isinstance(v._default, Sequence):
                        if not v._default.alias:
                            v._default.alias = cls.__alias__

                    if not v._name: v._name = k
                    cls._basic_fields[k] = v._name
                    cls._basic_sdleif[v._name] = k

                    if v._pk: cls._pk.append(k)

                cls._fields[k] = v

        return cls


#==============================================================================
class AvtukObject(DHTMLX_Render, object):
    __metaclass__ = AvtukMetaObject
    __live__ = 0
    __alias__ = ''
    __table__ = ''
    __order__ = ''

    __re_ord = re.compile(ur'(?i)order by ')

    def __repr__(self):
        return '<%s [%s] %s>' % (self.__class__.__name__, self._uin,
                                 ', '.join('%s=%s' % (i, self.values[i]) for i in self._basic_fields.keys()))


    def __init__(self, uin='', **kw):
        '''Параметры при инициализации через Executor
        uin - id в кэше
        fields - список названий полей
        val - список значений полей
        '''
        self._uin = uin
        self._dirty = []  # список измененных атрибутов
        self.values = dict([(i, None) for i in self._fields.keys()])
        self.old_values = self.values.copy()

#        print 'KF1', kw
#        if kw['data']:
#            print 'KF2', kw['data']

        if 'fields' in kw:
            for i, j in enumerate(kw['fields']):
                if j in self._basic_sdleif:
                    k = self._basic_sdleif[j]
                    self.values[k] = kw['data'][i]
                    self.old_values[k] = kw['data'][i]

    def __getitem__(self, attr): return self.__getattr__(attr)

    def __getattr__(self, attr):
        # обычные поля
        if attr in self._basic_fields:
            return self.values[attr]

        # внешние поля
        elif attr in self._reference_fields:
            if not self.values[attr]:
                self.values[attr] = self._fields[attr](self)
            return self.values[attr]

        # self.attr
        else:
            return object.__getattr__(self, attr)

    def __setattr__(self, attr, val):
        if attr in self._basic_fields:
            self.old_values[attr] = self.values[attr]
            self.__add_dirty(attr)
            self.values[attr] = val

        # внешние поля
        elif attr in self._reference_fields:
            if self.values[attr] != val:
                # TODO: добавить изменение ключевого поля
                self.values[attr] = val

        # self.attr
        else:
            object.__setattr__(self, attr, val)

    def __delattr__(self, attr):
        if attr not in self._basic_fields:
            del self.__dict__[attr]


    def __add_dirty(self, attr):
        if attr not in self._dirty:
            self._dirty.append(attr)


#    @classmethod
#    def __generate_sql(cls, kw):
#        # condition
#        cond = kw.pop('condition', '')
#        w1 = ' '.join(cls._basic_fields.get(i[1], i[1]) if i[0] == 1 else i[1] for i in generate_tokens(iter([cond]).next))
#        # key=val
#        w2 = ' AND '.join('%s = :%s' % (cls._basic_fields[i], i) for i in kw if i in cls._basic_fields)
#
#        w = w1 + (' AND ' if w1 and w2 else '') + w2
#        if w:
#            w = 'WHERE ' + w
#
#        order = kw.pop('order', cls.__order__)
#        if order: order = 'ORDER BY ' + order
#
#        return 'SELECT %s FROM %s %s %s' % (','.join(cls._basic_fields.values()), cls.__table__, w, order)


    @classmethod
    def _read(cls, multi, **kw):
        # def _read(cls, multi, sql='', **kw):
        kw.setdefault('live', cls.__live__)
        kw.setdefault('alias', cls.__alias__)

        _sql = kw.pop('sql', '')
        cond = kw.pop('condition', '')
        if not _sql:
            # condition
            w1 = (' '.join(cls._basic_fields.get(i[1], i[1]) if i[0] == 1 else i[1] for i in generate_tokens(iter([cond]).next))).replace(': ', ':')

            # key=val
            w2 = ' AND '.join('%s = :%s' % (cls._basic_fields[i], i) for i in kw if i in cls._basic_fields)
            w = w1 + (' AND ' if w1 and w2 else '') + w2
            if w: w = 'WHERE ' + w
            _sql = 'SELECT %s FROM %s %s' % (','.join(cls._basic_fields.values()), cls.__table__, w)

        order = kw.pop('order', cls.__order__)
        if multi and order and not cls.__re_ord.search(_sql):
            _sql = _sql + ' ORDER BY ' + ' '.join(cls._basic_fields.get(i[1], i[1]) if i[0] == 1 else i[1] for i in generate_tokens(iter([order]).next))

        # logging.info(_sql)
        return Executor.exec_cls(_sql, cls=cls, multi=multi, **kw)


    @classmethod
    def get(cls, condition='', **kw): return cls._read(False, condition=condition, **kw)


    @classmethod
    def select(cls, condition='', **kw): return cls._read(True, condition=condition, **kw)


    def save(self, **kw):
        isnew = kw.pop('isnew', any(self.values[i] is None for i in self._pk))

        if self._dirty or isnew:
            # set default volumes
            for i in self._basic_fields.keys():
                if self.values[i] is None:
                    x = self._fields[i]._default
                    if isinstance(x, (FunctionType, MethodType, BuiltinFunctionType, BuiltinMethodType,)):
                        x = x()

                    elif isinstance(x, Sequence):
                        # print 'W1', x
                        x = x()
                        # print 'W2', x

                    self.__setattr__(i, x)

            kw = {'alias': self.__alias__}
            if isnew:
                fields = []
                for i in self._dirty:
                    k = self._basic_fields[i]
                    kw[k] = self.values[i]
                    fields.append(k)

                sql = 'INSERT INTO %s (%s) VALUES (%s)' % (self.__table__,
                                                         ','.join(fields),
                                                         ','.join(' :%s' % i for i in fields))
            else:
                sets = []
                whr = []
                for i in self._dirty:
                    k = self._basic_fields[i]
                    kw[k] = self.values[i]
                    sets.append('%s = :%s' % (k, k))

                for pk in self._pk:
                    k = self._basic_fields[pk]
                    kw[k] = self.old_values[pk]
                    whr.append('%s = :%s' % (k, k))

                sql = 'UPDATE %s SET %s WHERE %s' % (self.__table__,
                                                     ', '.join(sets),
                                                     ' AND '.join(whr))

            self._dirty = []
            kw['uin'] = self._uin
            Executor.save(sql, **kw)



    def delete(self):
        kw = dict((self._basic_fields[i], self.values[i])  for i in self._pk)
        kw['multi'] = None
        kw['alias'] = self.__alias__
        kw['uin'] = self._uin

        w = ' AND '.join('%s = :%s' % (self._basic_fields[i], i) for i in self._pk)
        if w:
            w = 'WHERE ' + w

        Executor.save('DELETE FROM %s %s' % (self.__table__, w), **kw)


    def as_json(self, *fields, **kw):
        ''' Возвращает словарь свойств объекта. 
            Свойства как могут быть простыми - "id", так и сложными - "users_cls.name"
            @param fields - список полей (свойств)
            @param params - словарь алиасов полей (свойств).
                params['strftime'] - DataTime format
        '''
#        strftime = params.pop('strftime', None)
#        trailer = params.pop('trailer', {})
        show = kw.pop('show', {})

        if not fields:
            # fields = [k for k, v in self.values.items() if not isinstance(v, (MethodType, FunctionType))]
            fields = self.values.keys()
            
                    

        ret = {}
        for i in fields:
            try:
                val = self
                for k in i.split('.'): val = val.__getattr__(k)
            except: val = ''

            if i in show:
                try: val = show[i](val)
                except: pass

            if val is None:
                val = ''

            # print 'R', i, self._fields[i]
            
            def_str = str(val)

            if len(def_str) > 2 and ord(def_str[-1]) == 0:
                # print len(def_str)
                def_str = def_str[:-1]
                # print len(def_str)
                
            
            ret[kw.get(i, i)] = def_str
            
            if kw.get(i, i).endswith('name'):
                ret[kw.get(i, i).replace('.', '_')] = def_str  # str(val)

#        ret.update(trailer)
        return ret
