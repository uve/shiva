# coding: utf-8

from avtuk.render import DHTMLX_Render

#=============================================================================#
class SWCLS(DHTMLX_Render, object):
    # def __init__(self, uid, fields, val):
    def __init__(self, uid, **kw):
        '''
        uid - id в кэше
        fields - список названий полей
        val - список значений полей
        '''
        self._uid = uid
        self._fields = kw['fields']
        self.values = dict([(j, kw['data'][i]) for i, j in enumerate(self._fields)])


    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__,
                            ', '.join('%s=%s' % (k, v) for k, v in self.values.items()))

    def __getattr__(self, attr):
        # обычные поля
        if attr in self.values:
            return self.values[attr]

        # self.attr
        else:
            return object.__getattr__(self, attr)


    def __getitem__(self, attr): return self.__getattr__(attr)

    def as_json(self, *fields, **kw):
        ''' Возвращает словарь свойств объекта. 
            Свойства как могут быть простыми - "id", так и сложными - "users_cls.name"
            @param fields - список полей (свойств)
            @param kw - словарь алиасов полей (свойств).
                kw['strftime'] - DataTime format
        '''
#        trailer = params.pop('trailer', {})
        show = kw.pop('show', {})
        ret = {}

        if not fields:
            # fields = [k for k, v in self.__dict__.items() if not isinstance(v, (types.MethodType, types.FunctionType)) ]
            fields = self.values.keys()

        for i in fields:
            try:
                val = self
                for k in i.split('.'): val = val.values[k]
                    # val = val.__dict__[k]
            except: val = ''

            if i in show:
                try: val = show[i](val)
                except: pass

            if val is None:
                val = ''

            ret[kw.get(i, i)] = str(val)

#        ret.update(trailer)

        # print 'R', ret
        return ret

