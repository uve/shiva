# coding: utf-8

'''Модели для ORMа'''


import datetime
import settings as config
from avtuk.columns import Reference, Col, Executor
from avtuk.engine import AvtukObject, Reference, Sequence, Executor
from core.sw_base import md5passw
from barcode.zek_model import barcode2depart_sid

from tornado import template
from settings import TEMPLATE_DIR, DEFAULT_CLIENT


import cx_Oracle
import pytils



#=============================================================================#
 
class AssemblyList(AvtukObject):
    '''Сборочный лист'''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_header_recordp'

 
 
    ''' Печать Документов '''
    oper = 0
    ds = datetime.datetime.now().date() 
    de = datetime.datetime.now().date()
    
    head = 0
    header = None

    def __init__(self, input=None, rc=None):
                        
        # .data[0].values
        self.head = int(input["head"])
        preheader = Header.get_item(item_id=self.head, rc=rc).as_json('id', 'num', 'date', 'client_to_cls.name', 'client_from_cls.name',
                                                                 'client_to_cls.region_cls.name',
                                    show={'date':lambda val: val.strftime("%d.%m.%Y")})

        if not preheader:
            return             
        
        self.header = preheader[0]

    
    
    def as_print(self, mode=4):
        
        
        # список департаментов
        sql = '''SELECT DISTINCT r.depart, d.name
                 FROM factura f
                 JOIN recordp r ON f.id = r.factura
                 JOIN depart d ON r.depart=d.depart
                 WHERE f.header=:head AND d.depart_type<>3'''

        x = Executor.exec_cls(sql, head=self.head, multi=True)
                
        result = [AssemblyListPage(depart_id=v.depart, depart_name=v.name, head=self.head).as_data() for v in x.data]

                
        

        
        sql = '''select max(m_end) mend from packlist where factura=:head and palete is not Null'''
        
        max_number = Executor.exec_cls(sql, head=self.head, multi=False)
        
        
        if max_number["mend"]:
            max_number = max_number["mend"]
        else:
            max_number = ""    
        
        loader = template.Loader(TEMPLATE_DIR)
        output = loader.load("assembly_list.html").generate(data=result, header=self.header, max_number=max_number)
    
        # return output
        
        output = output.replace('\n', '').replace('\r', '')
                
        return {'cmd':'''self.Incunable(function(doc){ doc.write('%s') })''' % output} 
            
               
        """                
        total = sum(d.values["valume"] for d in result.data)

        loader = template.Loader("src\\shiva\\templates")        
        output = loader.load("waybill.html").generate(data=result.data, header=self.header, total=total)
    
        output = output.replace('\n', '').replace('\r', '')
                
        return {'cmd':'''self.Incunable(function(doc){ doc.write('%s') })''' % output} 
        """
 

#=============================================================================#
class AssemblyListPage(AvtukObject):
    
    depart_id = ""
    depart_name = ""
    head = ""
        
    bar_url = ""
    count_i = 0
    count_b = 0
            
    def __init__(self, depart_id=None, depart_name=None, head=None):
        
        self.depart_id = depart_id
        self.depart_name = depart_name
        self.head = head
        
        
        self.bar_url = '/warehouse/printpassport/data/image?mode=4&head=%s&depart=%s' % (self.head, self.depart_id)
        self.count_i = 0
        self.count_b = 0
        
        
        '''
        self.item = '%s/%s' % (i1, i2)
        
        self.head_num = header.num
        self.assemble_date = header.date.strftime("%d.%m.%Y")
        self.head_client = header.client_to_cls.name
        self.head_adr = header.client_to_cls.region_cls.name
        
        self.bar_url = '/warehouse/printpassport/data/image?mode=4&head=%s&depart=%s' % (header.id, depart_id,)
        '''
        
    def as_data(self):
            
        sql = '''SELECT valume, name, num, code, tpname, FLOOR(valume/inbox) box, valume-inbox*FLOOR(valume/inbox) piece, 
  CASE
    WHEN inbox > valume THEN NULL
    WHEN valume/inbox-FLOOR(valume/inbox) = 0 THEN TO_CHAR(FLOOR(valume/inbox))||'*'||TO_CHAR(inbox)
    ELSE TO_CHAR(FLOOR(valume/inbox))||'*'||TO_CHAR(inbox)||'+'||TO_CHAR(valume-inbox*FLOOR(valume/inbox))
  END  valume_box
FROM ( SELECT ABS(rp.valume) valume, t.name, shiva.GetPartyInBox(party.party) inbox, party.num, t.code, tp.name tpname
       FROM tehno.recordp rp, tovar t, party, tovar_place tp
       WHERE t.id=rp.tovar AND
             rp.party =party.party(+) AND
             rp.depart=:depart AND
             isclad.GetNewForOldTovar(t.id)=tp.tovar(+) AND (tp. name=(SELECT (MIN(name)) FROM tovar_place where tovar=isclad.GetNewForOldTovar(t.id) AND depart=rp.depart AND storage=0)
             ) AND rp.factura in (SELECT id FROM factura WHERE header=:head)
            AND rp.depart=tp.depart
       UNION
       SELECT ABS(rp.valume) valume, t.name, shiva.GetPartyInBox(party.party) inbox, party.num, t.code, '' tpname
       FROM tehno.recordp rp, tovar t, party, tovar_place tp
       WHERE t.id=rp.tovar AND
             rp.party =party.party(+) AND
             rp.factura IN (SELECT id FROM factura WHERE header=:head) AND
             rp.depart=:depart
             AND NOT EXISTS (SELECT * FROM tovar_place WHERE tovar=isclad.GetNewForOldTovar(t.id) AND depart=rp.depart AND storage=0)
)
        ORDER BY tpname,name '''
        # pytilswhere rownum<=2 ORDER BY tpname,name '''
        data = Executor.exec_cls(sql, head=self.head, depart=self.depart_id, multi=True).data
        
        self.count_i = 0
        self.count_b = 0

        
        for j, i in enumerate(data):
            self.count_i += i.piece
            self.count_b += i.box
            
        
        result = {  'depart_id':    self.depart_id,
                    'depart_name':  self.depart_name,
                    'head':         self.head,
                    'count_i':      self.count_i,
                    'count_b':      self.count_b,
                    'bar_url':      self.bar_url,
                    'data':         data,
                  }
        return result
                
        
    def as_print2(self):

        ret = []
        for j, i in enumerate(self.data):
            self.count_i += i.piece
            count_is = '<br />' if i.valume is None else i.valume

            self.count_b += i.box
            count_bs = '<br />' if i.valume_box is None else i.valume_box

            ret.append('<tr><td class="ast2f1">%s</td><td class="ast2f2">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (j + 1, i.tpname, count_is, count_bs, i.num, i.code, i.name))
            

        return ''.join(ret) 

    def table(self):

        ret = []
        for j, i in enumerate(self.data):
            self.count_i += i.piece
            count_is = '<br />' if i.valume is None else i.valume

            self.count_b += i.box
            count_bs = '<br />' if i.valume_box is None else i.valume_box

            ret.append('<tr><td class="ast2f1">%s</td><td class="ast2f2">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (j + 1, i.tpname, count_is, count_bs, i.num, i.code, i.name))
            

        return ''.join(ret) 





class Document(AvtukObject):
    ''' Печать Документов '''
    oper = 0
    ds = datetime.datetime.now().date() 
    de = datetime.datetime.now().date()
    
    head = 0
    header = None
    needre = []
    
    client_from = None
    client_to = None
    
    
    
    def __init__(self, input=None, rc=None):
                        
                        
        # .data[0].values
        self.head = int(input["head"])
        m_header = Header.get_item(item_id=self.head, rc=rc)
        
        preheader = m_header.as_json('id', 'num', 'numb', 'numb_in', 'date',
                                     'client_to', 'client_from', 'client_to_cls.name', 'client_from_cls.name',
                                    show={'date':lambda val: val.strftime("%d.%m.%Y")})

        # preheader = m_header.as_json(show={'date':lambda val: val.strftime("%d.%m.%Y")})

        if not preheader:
            return   
        
        self.header = preheader[0]
    
        self.client_from = Client.get(pClient=self.header["client_from"])
        self.client_to = Client.get(pClient=self.header["client_to"])

        sql = "select needre from client where id=:client_to"
        
        res = Executor.exec_cls(sql, client_to=self.header["client_to"], multi=False).as_json()
        
        if res["needre"] == "*":
      
            sql = '''select t.name, t2.nameser||' № '||t2.numser name1,
                   decode(trunc(t2.datas),'01.01.1900','Без срока',trunc(t2.datas)) datas,
                   t2.vidal
                    from  tovar t 
                    join  tovar t2 on t.sert=t2.id 
                    join  factura f on isclad.GetTovarFromModify(f.tovar)=t.id
                    where f.header=:pHeader 
                    union
                    select t.name, t2.nameser||' № '||t2.numser name1,
                           decode(trunc(t2.datas),'01.01.1900','Без срока',trunc(t2.datas)) datas,
                           t2.vidal
                    from factura f  
                    join  recordt r on r.factura=f.id
                    join  tovar t on r.tovar=t.id
                    join  tovar t2 on t.sert=t2.id 
                    where f.header=:pHeader'''
        
            self.needre = Executor.exec_cls(sql, pHeader=self.head, multi=True).as_json()
                
        pass
    
    

    def print_bill_and_factura(self):


        
        
        client = Client.get(pClient=DEFAULT_CLIENT)
        
        # № -     header.numb
        # "от:" - tsclad.datatovarheader(header.id
                                        
                                    
        ot = self.cursor.callfunc('tsclad.datatovarheader', returnType=cx_Oracle.DATETIME, parameters=[self.head]).strftime("%d.%m.%Y")                                   
 
  
        sql = '''select id,code,name,valume,round(summ_nds*100/118/valume,2) price,summ_nds,round(summ_nds*18/118,2) nds,
                 round(summ_nds*100/118,2) summ,npack from
                 (select f.id,t.code,t.name,p.n_short npack,f.valume,tsclad.GetFacturaBuhPrice(f.id) price,
                  tsclad.GetFacturaBuhPrice(f.id)*f.valume summ_nds
                  from factura f 
                  join tovar t on t.id=isclad.GetTovarFromModify(f.tovar)
                  left join pack p on p.id=t.pack
                  where header=:pHeader) 
                 order by name'''
        
        result = Executor.exec_cls(sql, pHeader=self.head, multi=True)
        
        total = 0
        
        try:
            total = sum(d.values["valume"] for d in result.data)
        except:
            self.write({'error':'Ошибка в товарной накладной'})
            return        
    

        loader = template.Loader(TEMPLATE_DIR)   
        
        m_total = pytils.numeral.in_words(len(result.data))
        m_summ_words = pytils.numeral.rubles(sum(item.values["summ_nds"] for item in result.data))  
        
        # factura
        # waybill_product.html     
        output = loader.load("waybill_all.html").generate(data=result.data, needre=self.needre, header=self.header,
                                                              total=total, client=client,
                                                              client_from=self.client_from, client_to=self.client_to,
                                                              ot=ot, m_total=m_total, m_summ_words=m_summ_words)
    
        output = output.replace('\n', '').replace('\r', '')
                
        return {'cmd':'''self.Incunable(function(doc){ doc.write('%s') })''' % output}    
        
    
    

    def print_internal_transfer(self):
        
        
        

        
        sql = '''select c.name,s.name sname,b.okpo,b.okud,b.chief from client c
                 join sklads s on c.contract=s.enterprise
                 join bank b on b.client=c.id
                 where s.type||s.contract=(select contract from client where id=:pClient)'''
        
        
        
        
        client = Executor.exec_cls(sql, pClient=self.header["client_to"], multi=False).as_json()
        # Номер header.numb_in
        # Дата  tsclad.datatovarheader(header.id)

        try:
            datatovarheader = self.cursor.callfunc('tsclad.datatovarheader', returnType=cx_Oracle.DATETIME, parameters=[self.head])
                 
            ot = datatovarheader.strftime("%d.%m.%Y")
        except: 
            ot = ""
        
                                           
 
        sql = '''select id,name,npack,valume,price,price*valume summ
                 from
                (select f.id,t.name,p.n_short npack,f.valume,tsclad.GetOurProviderOrPrice(t.id,h.data,1)  price
                 from factura f
                 join header h on h.id=f.header 
                 join tovar t on t.id=isclad.GetTovarFromModify(f.tovar)
                 left join pack p on p.id=t.pack
                 where h.id=:pHeader) 
                order by name'''

        result = Executor.exec_cls(sql, pHeader=self.head, multi=True)             
                   
        m_summ_words = pytils.numeral.rubles(sum(item.values["summ"] for item in result.data))                  
                
        loader = template.Loader(TEMPLATE_DIR)        
        output = loader.load("internal_transfer_all.html").generate(data=result.data, needre=self.needre, header=self.header,
                                                                    client_from=self.client_from, client_to=self.client_to,
                                                                    client=client, ot=ot, m_summ_words=m_summ_words)
    
        output = output.replace('\n', '').replace('\r', '')
        
        # f = open('text.html', 'w+')
        # f.write(output)
        # f.close()
         
        # return {'info':'done'}         
        return {'cmd':'''self.Incunable(function(doc){ doc.write('%s') })''' % output}    
                    
    
    
    def print_way_bill(self):
        
        sql = '''SELECT ID,HEADER,TOVAR,VALUME,PRICE,POINT POINT,DISCOUNT,KOEFF,PRICENDS,
                 SFMONEY,SMONEY,DMONEY,PRICEWNDS,SPOINT,KPACK,SPACK,SITOGOWNDS,NDS,SITOGO,
                 PLC,PNMB+P_NEW PNMB,RONMB RONMB,RONPP RONPP,KOMMB KOMMB,SPLC,SPNMB,CODE,NTOVAR,
                 WEIGHT,BUHPRICE,BUHSITOGOWNDS,NO_NDS,CTOVAR,sclad.GetPrice(wf.tovar,'R') pricer, 
                 our_provider_price,price_kz 
                 FROM tehno.W_Factura wf
                 WHERE Header = :pHeader
                 ORDER BY ntovar'''

        result = Executor.exec_cls(sql, pHeader=self.head, multi=True)
        
        
        total = sum(d.values["valume"] for d in result.data)

        loader = template.Loader(TEMPLATE_DIR)        
        output = loader.load("waybill.html").generate(data=result.data, needre=self.needre, header=self.header,
                                                      client_from=self.client_from, client_to=self.client_to,
                                                      total=total)
    
        output = output.replace('\n', '').replace('\r', '')
        

                
        return {'cmd':'''self.Incunable(function(doc){ doc.write('%s') })''' % output}       
    
    def as_print(self, mode=4):
        
        '''
           - если header.numb is not null
        
              -(1) и header.numb_in is null, то
        
               печатать Счет-фактуру и Товарную накладную.
        
              -(2) и header.numи_in is not null, то
        
               печатать Внутренее перемещение
        
           -(3) иначе (header.numb is null),то
             печатать Накладную, которая печатается сейчас поданному пункту            
        '''
        
        #if not self.header:
        #    return 

                        
        if 'numb' in self.header:           
            if 'numb_in' in self.header:
                return self.print_internal_transfer()
            else:
                return self.print_bill_and_factura()
        else:
            return self.print_way_bill()
                    
        return
 
 





class Package(AvtukObject):
    ''' Печать Упаковочного листа '''
    oper = 0
    ds = datetime.datetime.now().date() 
    de = datetime.datetime.now().date()
    
    head = 0
    header = None
    needre = []
    
    client_from = None
    client_to = None
    
    def __init__(self, input=None, rc=None):
                        
        # .data[0].values
        self.head = int(input["head"])
        m_header = Header.get_item(item_id=self.head, rc=rc)
        
        preheader = m_header.as_json('id', 'num', 'numb', 'numb_in', 'date',
                                     'client_to', 'client_from', 'client_to_cls.name', 'client_from_cls.name',
                                    show={'date':lambda val: val.strftime("%d.%m.%Y")})

        # preheader = m_header.as_json(show={'date':lambda val: val.strftime("%d.%m.%Y")})
        
        if not preheader:
            return     
    
        self.header = preheader[0]
        
        self.client_from = Client.get(pClient=self.header["client_from"])
        self.client_to = Client.get(pClient=self.header["client_to"])

        sql = "select needre from client where id=:client_to"
        
        res = Executor.exec_cls(sql, client_to=self.header["client_to"], multi=False).as_json()
        
          
  
    
    def as_print(self):
        
        sql = '''select id,tovar,factura,valume,to_char(mesto) mesto,weight,sotrud,
                sotrudp,code,prim,name,box,part from(
                select pl.id,pl.tovar,pl.factura,abs(pl.valume) valume,
                case when m_start=m_end then to_char(m_start)
                     when mesto<>0 then to_char(mesto)
                     else to_char(m_start)||'-'||to_char(m_end)
                end mesto, pl.weight,pl.sotrud,pl.sotrudp,t.code,pl.prim,t.name,pl.part,pl.box
                 from packlist pl 
                 join tovar t on pl.tovar=t.id 
                and pl.factura=:pHeader order by part,m_start,pl.mesto)'''

        result = Executor.exec_cls(sql, pHeader=self.head, multi=True)
        
        
        total_valume = sum(d.values["valume"] or 0 for d in result.data)
        total_weight = sum(d.values["weight"] or 0 for d in result.data)

        loader = template.Loader(TEMPLATE_DIR)        
        output = loader.load("package.html").generate(data=result.data, needre=self.needre, header=self.header,
                                                      client_from=self.client_from, client_to=self.client_to,
                                                      total_valume=total_valume, total_weight=total_weight)
    
        output = output.replace('\n', '').replace('\r', '')
        
        # return output
        # output = 'hello'

                
               
        return {'cmd':'''self.Incunable(function(doc){ doc.write('%s') })''' % output}  
 
 
 
 
 
#=============================================================================#
class ShivaException(Exception):
    ''' Базовый эксепшин для Шивы '''

class NotInPeriodException(ShivaException):
    ''' Юзверь есть но в смене его нет '''

class NotUserException(ShivaException):
    ''' Юзверь не найден '''


#=============================================================================#
class Period(AvtukObject):
    ''' Список смен '''
    __alias__ = 'tehno'
    __live__ = 0  # 60
    __table__ = 'period'

    id = Col(name="period", primary=True, default=Sequence('SQPERIOD'))
    date = Col(name='data', default=datetime.datetime.now)  # Дата начала смены
    date_end = Col(name='data_end')  # Дата окончания смены
    tsmena = Col(default=1)  # Тип смены
    tsmena_cls = Reference('TypeSmena', condition='Period.tsmena = TypeSmena.id')  # Тип смены
    rc = Col()  # Код РЦ
    current_tasks = Reference('Task', generator='gen_tasks_cls', multi=True)  # Текущие задания

    def gen_tasks_cls(self):
        t2 = (self.date - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')

        if config.FOR_TESTING:
            
            return '''SELECT * FROM sw_task
                  WHERE expose_task >=  TO_DATE('%s' ,'YYYY-MM-DD HH24:MI:SS') AND end_task IS NULL AND for_testing = 1 
                  ORDER BY id''' % t2, {}
        else:
            return '''SELECT * FROM sw_task
                  WHERE expose_task >=  TO_DATE('%s' ,'YYYY-MM-DD HH24:MI:SS') AND end_task IS NULL AND for_testing IS NULL
                  ORDER BY id''' % t2, {}
            

    @classmethod
    def get_last_smen(cls, rc):
        sql = '''SELECT * FROM period
                 WHERE data=(SELECT max(data) FROM period 
                             WHERE data_end IS NULL AND rc=:rc)
                   AND rc=:rc'''

        return cls.get(sql=sql, rc=rc)



#=============================================================================#
class RC(AvtukObject):
    ''' Справочник РЦ '''
    __alias__ = 'tehno'
    __live__ = 0#3600
    __table__ = 'distribution_center'

    id = Col(primary=True)
    name = Col(length=250)
    depart_cls = Reference('Department', condition='RC.id = Department.rc', multi=True)

    @classmethod
    def get_current(cls, rc):
        return cls.get(id=rc)


#=============================================================================#
class Department(AvtukObject):
    ''' Справочник участков '''
    __alias__ = 'tehno'
    __live__ = 0
    __table__ = 'depart'

    id = Col(name='depart', primary=True, default=Sequence('SQDEPART'))
    name = Col(length=50)
    rc = Col()
    rc_cls = Reference('RC', condition='RC.id = Department.rc')  # РЦ

#    #all_users_cls = Reference('User', condition='User.depart = Department.id', doc='Все сотрудники подразделения', multi=True)
    users_cls = Reference('User', generator='gen_user_cls', multi=True)

    def gen_user_cls(self):
        return '''SELECT * 
                  FROM sotrud
                  WHERE sotrud.depart = :dep AND sotrud.VISIBLE=1
                  ORDER BY name''', {'dep': self.id}


#=============================================================================#
class User(AvtukObject):
    ''' Список сотрудников '''
    __alias__ = 'tehno'
    __live__ = 0#120
    __table__ = 'sotrud'

    id = Col(primary=True, default=Sequence('SQSOTRUD'))
    sotrud = Col(length=20)
    name = Col(length=50)
    password = Col(length=50)
    visible = Col(default=1, show=lambda c, val : '' if val else 'уволен')
    depart = Col()
    depart_cls = Reference(Department, condition='User.depart = Department.id')
    role = Col()
    role_cls = Reference('Role', condition='User.role = Role.id')  # Основная роль
    current_role_cls = Reference('Role', generator='get_current_role')
    
    role = Col()

    def get_current_role(self):
        return '''SELECT * FROM sw_roles
                  WHERE id = ( SELECT UNIQUE CASE 
                                 WHEN s.role=1 THEN s.role
                                 WHEN h.role IS NOT NULL THEN h.role
                                 WHEN s.role IS NOT NULL THEN s.role  
                                 ELSE NULL
                               END
                               FROM sotrud s
                               LEFT JOIN sw_role_history h ON s.id=h.sotrud AND h.role_end IS NULL
                               WHERE s.id = :id AND ROWNUM<=1 )''', {'id': self.id}

    @classmethod
    def get_auth(cls, barcode, login='', passw=''):
        '''
        Авторизация.
        Проверяем по login, passw или по barcode и принадлежности к текущему РЦ.
        Потом или принадлежность к начальству или к текущей смене
        '''
        
        kw = {}
        
        # sql = 'SELECT * FROM sotrud'
        # user = Executor.exec_cls(sql)
        # print 'hello'
        
        sql = '''SELECT s.id, s.sotrud, s.name, s.depart, s.password, s.visible, s.ip, s.role, d.rc 
                 FROM sotrud s, depart d
                 WHERE s.visible=1 AND s.depart = d.depart'''# AND d.rc = :crc'''
        
        
        if login:
            sql = sql + ' AND s.sotrud = :sotrud AND s.password = :password'
            kw['sotrud'] = str(login).upper()
            kw['password'] = md5passw(kw['sotrud'], str(passw))
        elif barcode:
            barcode = barcode.replace("\n\r", "")
            sql = sql + ' AND s.depart = :depart AND s.id = :id'
            kw['depart'], kw['id'] = barcode2depart_sid(barcode)
        else:
            return None
        
        
        user = Executor.exec_cls(sql, multi=False, cls=cls, **kw)


        # юзер не найден
        if not user:
            raise NotUserException()

        return user


#=============================================================================#
class Role(AvtukObject):
    ''' Справочник ролей '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_roles'

    id = Col(primary=True)
    name = Col(length=50)
    device = Col()  # Наличие терминала сбора данных

    def set_modules(self, modules_on, modules_off):
        if modules_off:
            sql = '''DELETE FROM SW_ROLE_MODULE
                     WHERE ROLE_ID=%s AND MODULE_ID IN %s''' % (self.id, tuple(modules_off))
            Executor.exec_sql(sql, alias=self.__alias__)

        sql = '''MERGE INTO SW_ROLE_MODULE
                 USING DUAL ON (ROLE_ID=:role AND MODULE_ID=:module)
                 WHEN NOT matched THEN
                  INSERT(ROLE_ID,MODULE_ID) VALUES(:role, :module)'''
        for i in modules_on:
            Executor.exec_sql(sql, alias=self.__alias__, role=self.id, module=i)



#=============================================================================#
class RoleHistory(AvtukObject):
    ''' История ролей по сменам '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_role_history'

    id = Col(primary=True, default=Sequence('sqSW_ROLE_HISTORY'))
    sotrud = Col()
    period = Col()
    role_begin = Col(default=datetime.datetime.now)  # Время начала роли
    role_end = Col()  # Время окончания роли
    role = Col()



#=============================================================================#
class Menu(AvtukObject):
    ''' Список групп модулей '''
    __alias__ = 'tehno'
    __live__ = 0
    __table__ = 'sw_menu'

    id = Col(primary=True)
    name = Col(length=20)  # url меню
    caption = Col(length=20)  # Заголовок меню

    def modules_by_role(self, role):
        '''Разрешенные модули для http-меню'''
        sql = '''SELECT s.ID, s.CAPTION, s.DESCRIPTION, '/'||m.NAME||'/'||s.NAME url
                 FROM SW_MODULE s
                 JOIN sw_menu m ON s.SW_MENU_ID=m.ID AND m.NAME = :menu 
                 WHERE :role = 1 OR 
                       s.id IN ( SELECT MODULE_ID
                                 FROM SW_ROLE_MODULE
                                 WHERE ROLE_ID = :role )'''

        return [k.as_json() for k in Executor.exec_cls(sql, alias=self.__alias__, menu=self.name, role=role)]



#=============================================================================#
class Module(AvtukObject):
    ''' Список модулей '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_module'

    id = Col(primary=True)
    name = Col(length=20)  # url модуля 
    caption = Col(length=20)  # Заголовок модуля
    description = Col(length=50)  # Описание модуля
    menu = Col(name='sw_menu_id')  # Меню
    menu_cls = Reference(Menu, condition='Module.menu = Menu.id')  # Меню
    help = Col()

    def use_role(self, role_id):
        pass


#=============================================================================#
class TypeSmena(AvtukObject):
    ''' Справочник типов смен'''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'tsmena'

    id = Col(name='tsmena', primary=True, default=Sequence('SQTSMENA'))
    name = Col(length=30)  # Наименование


#=============================================================================#
class Pallet(AvtukObject):
    ''' Список палет '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_palete'

    id = Col(primary=True, default=Sequence('sqSW_PALETE'))
    party = Col(name='party_id')  # партия
    party_cls = Reference('Party', condition='Pallet.party = Party.id')  # Партия
    count = Col(name='valume', default=0)  # Количество товара
    depart = Col()  # Код отдела
    depart_cls = Reference(Department, condition='Pallet.depart = Department.id')  # Подразделение


#=============================================================================#
class PalletHistory(AvtukObject):
    ''' История перемещения палет '''
    __alias__ = 'tehno'
    __live__ = 10
    __table__ = 'palet_place'

    id = Col(primary=True, default=Sequence('sqPALET_PLACE'))
    header = Col()  # Фактура
    pallet = Col(name='palete')  # Палета
    pallet_cls = Reference('Pallet', condition='PalletHistory.pallet = Pallet.id')  # Палеты


#=============================================================================#
class Party(AvtukObject):
    ''' Партии товара '''
    __alias__ = 'tehno'
    __live__ = 10
    __table__ = 'party'

    id = Col(name='party', primary=True, default=Sequence('sqParty'))
    tovar = Col()  # Код товара
    tovar_cls = Reference('Tovar', condition='Party.tovar = Tovar.id')  # Товар
    date = Col(name='data')  # Срок годности
    num = Col()
    inbox = Col()
    

    d_iss = Col()

#=============================================================================#
class PartyTemp(AvtukObject):
    ''' распечатанные ID партий '''
    __alias__ = 'tehno'
    __live__ = 0
    __table__ = 'sw_party'

    id = Col(primary=True, default=Sequence('sqPARTY'))


class ExtraPartyTemp(AvtukObject):
    ''' распечатанные ID партий '''
    __alias__ = 'tehno'
    __live__ = 0
    __table__ = 'extra_party'

    id = Col(primary=True, default=Sequence('sqEXTRAPARTY'))

#=============================================================================#
class Tovar(AvtukObject):
    ''' Справочник товаров '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'tovar'

    id = Col(primary=True, default=Sequence('sqTovar'))
    name = Col(length=80)  # Название
    typet = Col()  # Тип товара
    typet_cls = Reference('TypeTovar', condition='Tovar.typet = TypeTovar.id')
    code = Reference(None, generator='gen_code')

    def gen_code(self):
        return 'select SUBSTR(isclad.GetTovarCodeFromModify(:id), 1, 25) from dual', {'id':self.id, 'alias':self.__alias__}

#=============================================================================#
class Status(AvtukObject):
    ''' Статус Header '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'status'

    id = Col(primary=True, default=Sequence('sqHEADER'))
    name = Col(length=30)


class Marsh(AvtukObject):
    ''' Статус Header '''
    __alias__ = 'tehno'
    __live__ = 0
    __table__ = 'mess_for_header'

    id = Col(primary=True)  # , default=Sequence('sqHEADER'))
    name = Col(length=30)

#=============================================================================#
class Header(AvtukObject):
    ''' Заголовок фактур '''
    __alias__ = 'tehno'
    __live__ = 5
    __table__ = 'header'

    id = Col(primary=True, default=Sequence('sqHEADER'))
    oper = Col()  # Код операции
    oper_cls = Reference('Oper', condition='Header.oper = Oper.id')  # Операция
    stage = Col()  # Стадия фактуры
    num = Col(length=10)  # Символьный номер
    numb = Col()  #
    numb_in = Col()  #
    date = Col(name='data')  # Дата
    status = Col(name='status')  # статус
    status_cls = Reference('Status', condition='Header.status = Status.id')
    client_from = Col(name='client_from')  # Код клиента продавца
    client_from_cls = Reference('Client', condition='Header.client_from = Client.id')  # Клиент продавец
    client_to = Col(name='client_to')  # Код клиента покупателя
    client_to_cls = Reference('Client', condition='Header.client_to = Client.id')  # Клиент покупатель
    os_numb = Col(name='os_numb')  # номер отправки
    pallet = Col(name='pallet')
    pallet_cls = Reference('PastingType', condition='Header.pallet=PastingType.id')  # тип оклейки

    PalletHistory_cls = Reference(PalletHistory, condition='PalletHistory.header = Header.id', multi=True)  # Все сотрудники подразделения
       
    marsh = Col()  #
    marsh_cls = Reference('Marsh', condition='Header.marsh = Marsh.id')
    
    storage = Col()        
    prim = Col()  #
    desk = Col()  #
    skin = Col()  # 
    

    @classmethod
    def get_item(cls, item_id=0, rc=None):
                        
        #sql = '''SELECT h.id, h.oper, h.stage, h.num, h.numb, h.numb_in, h.data, h.status, h.client_from, h.client_to,
        #                h.marsh, h.prim, ms.name marsh_name, h.storage, h.os_numb, h.desk, h.prim, h.skin
        #         FROM header h
        #         left join mess_for_header ms on ms.id=h.marsh
        #         JOIN depart ON depart.depart IN (SELECT depart FROM depart WHERE rc = :rc AND depart_type = 3)
        #         WHERE depart.depart IN (SELECT depart FROM shema WHERE oper=h.oper) AND h.id =:item_id'''
        
        
        sql = '''select h.id, h.oper, h.stage, h.num, h.numb, h.numb_in, h.data, h.status, h.client_from, h.client_to,
                   h.marsh, h.prim, ms.name marsh_name, h.storage, h.os_numb, h.desk, h.prim, h.skin
                    from header h
                    left join mess_for_header ms 
                    on ms.id=h.marsh               
                    where  h.id =:item_id'''

        return cls.select(sql=sql, item_id=item_id)  # , depart_type=depart_type)        

    @classmethod
    def _custom_select(cls, depart_type, opers, rc=None):
        '''
        :depart_type 1-приемка, 3-сборка, 6-БТК,  31- Участок приемки сырья
        :opers дополнительный WHERE
        '''
        sql = '''SELECT h.id, h.oper, h.stage, h.num, h.numb_in, h.data, h.status, h.pallet, h.os_numb, h.client_from, h.client_to, h.marsh, h.prim, h.storage      
                 FROM header h
                 JOIN shema  ON h.oper=shema.oper AND h.stage=shema.stage
                 JOIN depart ON depart.depart IN (SELECT depart FROM depart WHERE rc = :rc AND depart_type = :depart_type )
                 WHERE (shema.depart =depart.depart)'''

        if int(depart_type) == 1:
            sql = sql + ' AND (SELECT COUNT(*) FROM header_input WHERE headinput=h.id)=0 '

        # Без розничных продаж и подарков
        if int(opers) == 1:
            sql = sql + ' AND h.oper NOT IN (233,245,277,276)'
        # Только розничные продажи
        elif int(opers) == 2:
            sql = sql + ' AND h.oper in (233,245)'
        # Только подарки клиентам
        elif int(opers) == 3:
            sql = sql + ' AND h.oper in (277,276)'

        return cls.select(sql=sql, rc=rc, depart_type=depart_type)

    @classmethod
    def select_BTK(cls, opers, rc=None):
        return cls._custom_select(6, opers, rc)

    @classmethod
    def select_accept(cls, opers, rc=None):
        return cls._custom_select(1, opers, rc)

    #@classmethod
    #def select_assembly(cls, opers, rc=None):
    #    return cls._custom_select(3, opers, rc)

    @classmethod
    def select_passport(cls, opers, data_start, data_end, rc=None):
        sql = '''SELECT h.id, h.oper, h.stage, h.num, h.data, h.status, h.client_from, h.client_to      
                 FROM header h
                 JOIN depart ON depart.depart IN (SELECT depart FROM depart WHERE rc = :rc AND depart_type = 3)
                 WHERE depart.depart IN (SELECT depart FROM shema WHERE oper=h.oper) AND h.data BETWEEN :ds AND :de'''
        # AND h.id = '268231899' OR h.id = '268165799' 
        
        # Без розничных продаж и подарков
        if opers == 1:
            sql = sql + ' AND h.oper NOT IN (233,245,277,276)'
        # Только розничные продажи
        elif  opers == 2:
            sql = sql + ' AND h.oper in (233,245)'
        # Только подарки клиентам
        elif  opers == 3:
            sql = sql + ' AND h.oper in (277,276)'

        return cls.select(sql=sql, rc=rc, ds=data_start, de=data_end)




#=============================================================================#
class Oper(AvtukObject):
    ''' Справочник операций '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'oper'

    id = Col(name='oper', primary=True, default=Sequence('sqOper'))
    name = Col(length=50)  # Название


#=============================================================================#
class Region(AvtukObject):
    '''Города клиентов'''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'region'

    id = Col(name='region', primary=True)
    name = Col(length=30)  # Наименование


#=============================================================================#
class Client(AvtukObject):
    ''' Справочник клиентов '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'client'

    id = Col(primary=True, default=Sequence('sqClient'))
    name = Col(length=50)  # Наименование
    bank_cls = Reference('Bank', condition='Client.id = Bank.client')  # адрес
    region = Col()
    region_cls = Reference('Region', condition='Client.region = Region.id')  # город
    
    sender = Col()
    
    pClient = None


    # def __init__(self):
    #    pass
        
    @classmethod
    def get(self, pClient=None):

        sql = '''SELECT decode(c.prim,null,c.name,c.prim) name_full,
                b.inn,b.account,b.bank,b.korr,b.bic,okpo,b.okonh,b.phone,b.dogovorn,b.dogovork,
                b.accountant,b.chief,c.name,c.adress_ur,b.adress
                from client c 
                left join bank b on c.id=b.client 
                WHERE c.id=:pClient'''

        self.pClient = pClient
        
        result = Executor.exec_cls(sql, pClient=self.pClient, multi=False)
        if result:
            return result.as_json()
        
        return



#=============================================================================#
class ExportCell(AvtukObject):
    ''' Список изменений ячеек склада '''
    __alias__ = 'tehno'
    __live__ = 0
    __table__ = 'vw_export_cell'

    str = Col()
    begin_date = Col()  # Постановка задачи
    
    
    
#=============================================================================#
class Task(AvtukObject):
    ''' История заданий работникам склада '''
    __alias__ = 'tehno'
    __live__ = 0  # 5
    __table__ = 'sw_task'

    id = Col(primary=True, default=Sequence('sqSW_TASK'))
    sotrud = Col()  # Сотрудник
    sotrud_cls = Reference('User', condition='Task.sotrud = User.id')  # Сотрудник
    types_task = Col(name='id_types_task')  # Тип задачи
    types_task_cls = Reference('TypeTask', condition='Task.types_task = TypeTask.id')  # Типы заданий работникам склада
    expose_task = Col()  # Постановка задачи
    begin_task = Col()  # Начало исполнения
    end_task = Col()  # Окончание исполнения
    delegate_task = Col()
    
    id1 = Col()
    id2 = Col()


#=============================================================================#
class TypeTask(AvtukObject):
    ''' Типы заданий работникам склада '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_types_task'

    id = Col(primary=True, default=Sequence('sqSW_TYPES_TASK'))
    name = Col(length=50)  # Название


#=============================================================================#
class Cell(AvtukObject):
    ''' Справочник мест хранения '''
    __alias__ = 'tehno'
    __live__ = 0
    __table__ = 'tovar_place'
    __order__ = 'stelag, polka, place'

    id = Col(primary=True, default=Sequence('sqTOVAR_PLACE'))
    stelag = Col()  # стеллаж
    polka = Col()  # полка в высоту
    place = Col()  # ячейка
    depart = Col()  # Код отдела
    depart_cls = Reference(Department, condition='Cell.depart = Department.id')  # Подразделение


#=============================================================================#
class TypeTovar(AvtukObject):
    ''' Тип товара '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'type_tovar'

    id = Col(primary=True, default=Sequence('sqTypeTovar'))
    name = Col(length=50)

    @classmethod
    def select_life(cls):
        # sql = 'SELECT id FROM type_tovar WHERE dep IS NOT NULL AND hide=1 AND category not in (5,6)'
        
        sql = '''SELECT id FROM type_tovar WHERE dep IS NOT NULL AND hide=1 AND id not in (8, 54,56,58,60,61, 77,78,79, 110,111, 112, 116, 120,125,127,128,129,130,131,132,133,134,135,136,300000201,300002201)'''
        
        # sql = 'SELECT id FROM type_tovar WHERE hide=1'
        return cls.select(sql=sql)


#=============================================================================#
class FailCell(AvtukObject):
    ''' Заблокированные ячейки '''
    __alias__ = 'tehno'
    __live__ = 300
    __table__ = 'sw_failcell'

    id = Col(primary=True, default=Sequence('sqSW_FAILCEIL'))
    tovar_place = Col()
    tovar_place_cls = Reference(Cell, condition='FailCell.tovar_place = Cell.id')
    dstart = Col()
    typeblock = Col()
    sotrud = Col()
    sotrud_cls = Reference(User, condition='FailCell.sotrud = User.id')
    done = Col()
    palete = Col()
    valume = Col()
    party = Col()
    dend = Col()
    close_sotrud = Col()
    close_sotrud_cls = Reference(User, condition='FailCell.close_sotrud = User.id')

#=============================================================================#
class Factura(AvtukObject):
    ''' Состав заказа '''
    __alias__ = 'tehno'
    __live__ = 600
    __table__ = 'factura'

    id = Col(primary=True, default=Sequence('sqFactura'))
    header = Col()  # Код заголовка
    header_cls = Reference(Header, condition='Factura.header = Header.id')
    tovar = Col()  # Код товара
    tovar_cls = Reference(Tovar, condition='Factura.tovar = Tovar.id')
    count = Col(name='valume')  # Количество


#=============================================================================#
class Report(AvtukObject):
    ''' Справочник отчетов '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_reports'

    id = Col(primary=True, default=Sequence('sqSW_REPORTS'))
    name = Col(length=80)  # Название
    descript = Col()  # (CLOB) Описание отчета
    params = Col()  # (CLOB) Спек параметров
    src = Col()  # (CLOB) Исходник отчета
    rights = Col()  # Права: NULL-все, 0-свой РЦ, 1-свой отдел


#=============================================================================#
class Bank(AvtukObject):
    ''' Справочник отчетов '''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'bank'

    id = Col(primary=True, default=Sequence('sqBank'))
    client = Col()
    adress = Col(length=100)
    phone = Col(length=50)

#=============================================================================#
class ListAssembly(AvtukObject):
    '''Сборочный лист'''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_header_recordp'

    id = Col(primary=True, default=Sequence('sqsw_header_recordp'))
    header = Col()
    depart = Col()
    sotrud = Col()
    sotrudp = Col()
    data = Col()


#=============================================================================#
class PastingType(AvtukObject):
    '''Доп.информация по сборочным фактурам'''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_pasting_type'
    id = Col(primary=True)
    name = Col(name='name', length=64)  # Название


class StorageType(AvtukObject):
    '''Доп.информация по сборочным фактурам'''
    __alias__ = 'tehno'
    __live__ = 3600
    __table__ = 'sw_storage_type'
    id = Col(primary=True)
    name = Col(name='name', length=64)  # Название
