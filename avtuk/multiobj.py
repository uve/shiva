# coding: utf-8

# from urllib import quote
from avtuk.swcls import SWCLS
import datetime

#==============================================================================
class AvtukMultiObject(object):
    def __init__(self, uid, **kw):
        self._uid = uid
        cls = kw.pop('cls', SWCLS)
        self.max_record = kw['count']
        self.data = [cls(uid, fields=kw['fields'], data=i) for i in kw['data']]


    def __len__(self): return len(self.data)
    # def len(self):  return len(self.data)
    def __getitem__(self, i): return self.data[i]
    def __setitem__(self, i, item): self.data[i] = item
    def __delitem__(self, i): del self.data[i]
    def __repr__(self): return '<AvtukMultiObject %s>' % repr(self.data)
    def __lt__(self, other): return self.data < self.__cast(other)
    def __le__(self, other): return self.data <= self.__cast(other)
    def __eq__(self, other): return self.data == self.__cast(other)
    def __ne__(self, other): return self.data != self.__cast(other)
    def __gt__(self, other): return self.data > self.__cast(other)
    def __ge__(self, other): return self.data >= self.__cast(other)
    def __cast(self, other):
        if isinstance(other, AvtukMultiObject): return other.data
        else: return other
# ##    def __cmp__(self, other): return cmp(self.data, self.__cast(other))
#    __hash__ = None # Mutable sequence, so not hashable
    def __contains__(self, item): return item in self.data
    def __getslice__(self, i, j):
        i = max(i, 0); j = max(j, 0)
        return self.__class__(self.data[i:j])
    def __setslice__(self, i, j, other):
        i = max(i, 0); j = max(j, 0)
        if isinstance(other, AvtukMultiObject):
            self.data[i:j] = other.data
    def __delslice__(self, i, j):
        i = max(i, 0); j = max(j, 0)
        del self.data[i:j]
    def insert(self, i, item): self.data.insert(i, item)
    def pop(self, i=-1): return self.data.pop(i)
    def remove(self, item): self.data.remove(item)
    def count(self, item): return self.data.count(item)
    def index(self, item, *args): return self.data.index(item, *args)
    def extend(self, other):
        if isinstance(other, AvtukMultiObject):
            self.data.extend(other.data)
    def append(self, item): self.data.append(item)

    def save(self):
        for i in self.data: i.save()

    def as_json(self, *fields, **params):
        return [i.as_json(*fields, **params) for i in self.data]

    def as_grid(self, *fields, **kw):
        head = kw.get('head', False)

        udat = []

        for i in ['info', 'warning', 'error', 'cmd']:
            x = kw.pop(i, [])
            if x and isinstance(x, basestring): x = [x]
            udat += [(i, j) for j in x]

        if len(self.data) != self.max_record:
            udat.append(('warning', 'Слишком много данных (отображено %s из %s)' % (len(self.data), self.max_record)))

        if not fields and self.data:
            if isinstance(self.data[0]._fields, (list, tuple)):
                fields = self.data[0]._fields
            elif isinstance(self.data[0]._fields, dict):
                fields = self.data[0]._basic_fields.keys()

        if head == True:
            h = []

            for i in fields:
                x = self.data[0][i]

                if isinstance(x, basestring):
                    p = (190, 'left', 'str')
                elif isinstance(x, datetime.datetime):
                    p = (92, 'left', 'date')
                    kw.setdefault('show', {})
                    kw['show'][i] = lambda val: val.strftime("%d.%m.%Y %H:%M")
                else:
                    p = (50, 'right', 'int')

                h.append('<column width="%s" type="ed" align="%s" sort="%s">%s</column>' % (p + (i,)))

            head = '<head>%s</head>' % ''.join(h)


        return '<rows>%s%s%s</rows>' % (head,
                                        ''.join('<userdata name="%s"><![CDATA[%s]]></userdata>' % (i[0], i[1]) for i in udat),
                                        ''.join([i.as_grid(*fields, **kw) for i in self.data]))

    def as_combo(self, *fields, **kw):
        return '<complete>%s</complete>' % ''.join([i.as_combo(*fields, **kw) for i in self.data])

#    def as_form_combo(self, *fields, **params):
#        return '<data>%s</data>' % ''.join([i.as_form_combo(*fields, **params) for i in self.data])


def as_grid(self, *fields, **kw):
    head = kw.get('head', False)

    udat = []

    for i in ['info', 'warning', 'error', 'cmd']:
        x = kw.pop(i, [])
        if x and isinstance(x, basestring): x = [x]
        udat += [(i, j) for j in x]

    if len(self.data) != self.max_record:
        udat.append(('warning', 'Слишком много данных (отображено %s из %s)' % (len(self.data), self.max_record)))

    if not fields and self.data:
        if isinstance(self.data[0]._fields, (list, tuple)):
            fields = self.data[0]._fields
        elif isinstance(self.data[0]._fields, dict):
            fields = self.data[0]._basic_fields.keys()

    if head == True:
        h = []

        for i in fields:
            x = self.data[0][i]

            if isinstance(x, basestring):
                p = (190, 'left', 'str')
            elif isinstance(x, datetime.datetime):
                p = (92, 'left', 'date')
                kw.setdefault('show', {})
                kw['show'][i] = lambda val: val.strftime("%d.%m.%Y %H:%M")
            else:
                p = (50, 'right', 'int')

            h.append('<column width="%s" type="ed" align="%s" sort="%s">%s</column>' % (p + (i,)))

        head = '<head>%s</head>' % ''.join(h)


    return '<rows>%s%s%s</rows>' % (head,
                                    ''.join('<userdata name="%s"><![CDATA[%s]]></userdata>' % (i[0], i[1]) for i in udat),
                                    ''.join([i.as_grid(*fields, **kw) for i in self.data]))
