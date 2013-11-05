# coding: utf-8

__all__ = ('Col', 'Reference', 'Property')

from executor import Executor

#=============================================================================#
class CustomCol(object):
    def __init__(self, **kw):
        self._null = kw.pop('null', True)

#=============================================================================#
class Col(CustomCol):
    def __init__(self, **kw):
        self._name = kw.pop('name', None)
        self._default = kw.pop('default', None)
        self._pk = kw.pop('primary', False)
        self._len = kw.pop('length', None)
        self._show = kw.pop('show', None)

        # if 'from_DB' in kw: self.from_DB = kw['from_DB']
        # if 'to_DB' in kw: self.to_DB = kw['to_DB']

        CustomCol.__init__(self, **kw)

#    @staticmethod
#    def from_DB(self, prop_name, value): return value
#
#    @staticmethod
#    def to_DB(self, prop_name, value): return value


#==============================================================================
# class IntCol(Col):
#    @staticmethod
#    def from_DB(self, prop_name, value): return int(value)


#=============================================================================#
class ReferenceException(Exception):
    ''' Эксепшин для внешних полей '''

class Reference(CustomCol):
    def __init__(self, cls, **kw):
        '''arg variants:
        condition = 'RefCls.property = SelfCls.property'
        generator = function() -> SQL        
        '''
        self._cls = cls
        self._generator = kw.pop('generator', None)
        self._condition = kw.pop('condition', None)
        self._multi = kw.pop('multi', False)

    def __call__(self, parent):
        if isinstance(self._cls, basestring):
            self._cls = Executor.classes[self._cls]

        # codtition
        if self._condition:
            c1, c2 = [i.strip() for i in  self._condition.split('=')]

            if c2.startswith(parent.__class__.__name__ + '.'):
                c1, c2 = c2, c1

            c1a, c1b = c1.split('.')
            c2a, c2b = c2.split('.')

            if parent.__class__.__name__ <> c1a or self._cls.__name__ <> c2a:
                raise ReferenceException('Invalid condition "%s" by classes "%s" and "%s"' % (self._condition, c1, c2))

            return self._cls._read(self._multi, **{c2b:parent.values[c1b]})

        # if function of SQL generating 
        elif self._generator:
            if isinstance(self._generator, basestring):
                self._generator = parent.__class__.__dict__[self._generator]

            sql, kw = self._generator(parent)

            # None-классы т.е. SQL-функции
            if self._cls is None:
                return Executor.exec_sql(sql, multi=False, **kw).data[0]
            # Внешние классы
            else:
                return self._cls._read(self._multi, sql=sql, **kw)

#=============================================================================#
class Property(CustomCol):
    def __init__(self, function, **kw):
        pass

