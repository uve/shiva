# coding: utf-8

from urllib import quote
# from urllib.parse import quote

#=============================================================================#
class DHTMLX_Render(object):
    def as_xml(self, *fields, **kw):
        ''' Возвращает словарь свойств объекта в виде XML. 
            Свойства как могут быть простыми - "id", так и сложными - "users_cls.name"
            @param fields - список полей (свойств)
            @param params - словарь алиасов полей (свойств).
            Значение params['root'] используется в качестве имени Root node. 
            If value params['root'] = False (or ""), then Root node not renderig  
        '''
        root = kw.pop('root', 'data')
        ret = ''.join('<%s><![CDATA[%s]]></%s>' % (k, v, k) for k, v in self.as_json(*fields, **kw).items())
        r1, r2 = ('<%s>' % root, '</%s>' % root) if root else ('', '',)
        return '%s%s%s' % (r1, ret, r2)

    def as_json(self, *fields, **kw):
        ''' XML for DHTMLX Grid
            @param fields - cells
            @param kw - kw['id'] row id, 
                        kw['attr'] = [attributes]
        '''
        sid = kw.pop('id', 'id')
        attr = kw.pop('attr', [])

        fields2 = fields[:]


        if sid not in fields2: fields2 += (sid,)

        if attr: fields2 += tuple([i for i in attr if i not in fields2])
        return self.as_json(*fields2, **kw)
        

    def as_grid(self, *fields, **kw):
        ''' XML for DHTMLX Grid
            @param fields - cells
            @param kw - kw['id'] row id, 
                        kw['attr'] = [attributes]
        '''
        sid = kw.pop('id', 'id')
        attr = kw.pop('attr', [])

        fields2 = fields[:]


        if sid not in fields2: fields2 += (sid,)

        if attr: fields2 += tuple([i for i in attr if i not in fields2])
        js = self.as_json(*fields2, **kw)
        return '<row id="%s" %s>%s</row>' % (js[sid],
                                             ' '.join(['%s="%s"' % (i, quote(js[i]),) for i in attr]),
                                             ''.join('<cell><![CDATA[%s]]></cell>' % js[kw.get(i, i)] for i in fields))


    def as_combo(self, *fields, **kw):
        ''' XML for DHTMLX Combobox (<Select>)
            @param field - field value of Combo item 
            @param params:
                params['id'] id of Combo item
                params['delimiter'] values delimiter of Combo item
        '''
        sid = kw.pop('id', 'id')
        delimiter = kw.pop('delimiter', ' - ')

        fields2 = fields
        if sid not in fields2: fields2 += (sid,)
        js = self.as_json(*fields2, **kw)
        return '<option value="%s">%s</option>' % (js[sid], delimiter.join([js[kw.get(i, i)] for i in fields]))

#    def as_form_combo(self, *fields, **params):
#        ''' XML for DHTMLX Form Combobox (<Select>)
#            @param field - field value of Combo item 
#            @param params:
#                params['id'] id of Combo item
#                params['delimiter'] values delimiter of Combo item
#        '''
#        sid = params.pop('id', 'id')
#        delimiter = params.pop('delimiter', ' - ')
#
#        fields2 = fields
#        if sid not in fields2: fields2 += (sid,)
#        js = self.as_json(*fields2, **params)
#        return '<item value="%s" label="%s"></item>' % (js[sid], delimiter.join([js[params.get(i, i)] for i in fields]))

