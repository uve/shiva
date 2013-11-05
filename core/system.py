# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.executor import Executor

#=== Сообщения для правой панели десктоп-браузера =============================
class SystemMessageHandler(BaseHandler):
    urls = r'/system/message'

    def get(self):  

        if not self.session:
            return
        
        self.cursor.execute("select mess, 2 as type from header_message where usr=:user_id", user_id=str(self.session.uid))                        
        result = self.cursor.fetchall()
        
        self.write(result)





#=== Таблица в виде CSV =======================================================
class SystemCSVHandler(BaseHandler):
    urls = r'/system/csv'

    def post(self):
        inp = self.input(dat='', filename='')

        if inp.filename:
            self.write(inp.dat.decode('utf-8').encode('cp1251'))
            self.set_header("Content-Type", 'text/csv; charset=utf-8')
            self.set_header("Content-Disposition", 'attachment; filename="%s.csv"' % inp.filename)


#=== Чтение/Запись справки к модулям ==========================================
class SystemHelpHandler(BaseHandler):
    urls = r'/system/help/(.*)'

    def get(self, param):
        if not param:
            self.write('Введите штрих-код со своего бэйджика или свои логин и пароль, и нажмите кнопку "OK"')

        else:
            try:
                imen, imod = param.split('/')
                sql = '''SELECT help FROM sw_module
                         WHERE name = :imod
                           AND sw_menu_id = (SELECT id FROM sw_menu WHERE name = :imen)'''

                self.write(Executor.exec_sql(sql, multi=False, imen=imen, imod=imod)['data'][0].read())
            except:
                self.write('')


    def post(self, param):
        try:
            imen, imod = param.split('/')
            sql = '''UPDATE sw_module SET help = :hlp
                     WHERE name = :imod
                       AND sw_menu_id = (SELECT id FROM sw_menu WHERE name = :imen)'''
            Executor.exec_sql(sql, imen=imen, imod=imod, hlp=self.request.body)

            self.write({'info':'Информация сохранена'})
        except:
            self.write({'warning':'Ошибка записи'})



