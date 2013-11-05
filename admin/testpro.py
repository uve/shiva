# coding: utf-8

# import cStringIO, os.path, logging, Image, ImageFont, ImageDraw
from core.sw_base import BaseHandler


#==============================================================================
class AdminTestproHandler(BaseHandler):
    urls = r'/admin/testpro'

    def get(self):
        try:
            # print 'CU', self.cursor
            self.cursor.execute('select 1 from dual')
            for i in self.cursor.fetchall():
                print 'I', i


#            Ret = self.cursor.var(cx_Oracle.NUMBER)
#            cur.execute('''begin shiva.SetPalletPartyCell(:pallet, :party, :cell, :val, :plus, :Ret); end;''',
#                        pallet=inp.pallet, party=inp.party, cell=rec[0], val=int(inp.onpallet) * inboxcount, plus=inp.mode, Ret=Ret)
#
#            # отдадим результат - строчку пояснения, если что-то оказалось не так
#            if Ret.getvalue() == 0:
#                self.write(['OK'])
#            elif Ret.getvalue() == -1:
#                self.write(['ERROR', 'Такой паллеты не существует'])


            self.write({'info':"YEEEES" })
        except Exception, e:
            print 'EEE', e
            self.write({'error':"FIGU" })


#==============================================================================
class AdminTestproDataHandler(BaseHandler):
    # urls = r'/admin/testpro/data/([^/]+)'
    urls = r'/admin/testpro/data'

    # def get(self, param):
    def post(self):

#        if param == 'gts':
#            try:
#                ids = int(self.input(ids=0).ids)
#                ReferenceExec(self.application.connect, 'BEGIN tsclad.oksdelka(%s, 0); END;' % (ids))
#                self.write({'info':'Информация сохранена'})
#            except:
#                self.write({'warning':'Ошибка записи'})
        self.write({'info':'TEST'})
