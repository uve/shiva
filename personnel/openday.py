# coding: utf-8

from core.sw_base import BaseHandler

from avtuk.avtuk_models import TypeSmena, Role, Period, RoleHistory, User, RC


from avtuk.executor import Executor

#=== Правка смены =============================================================
class OpenDayHandler(BaseHandler):
    urls = r'/personnel/openday'

    def get(self):
        # кнопки с департаментами РЦ


        deps = RC.get_current().depart_cls
        bdep = [{"id":"dep%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_3"} for i in deps]
        
        
        period = Period.get_last_smen()

        tsmen = []
        for i in TypeSmena.select():
            x = {"id":"tsmen%s" % i.id, "type":"button", "text":i.name, "action":"do_tool_2"}
            if period and i.id == period.tsmena: x['selected'] = "true"
            tsmen.append(x)

        pid = period.id if period else 0
        pts = period.tsmena if period else 1
        pids = 'Правка смены:  %s' % period.date.strftime("%d.%m.%Y %H:%M") if pid else 'Открытие смены'
        rols = ','.join('[%s,"%s"]' % (i.id, i.name) for i in Role.select('id<>1'))

        self.write({'def':[{'type':"button", 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_1', 'text':'Сохранить' if pid else "Открыть смену"},
                           {'type':"separator"},

                           {'type':"text", 'text':"  Подразделение:"},
                           {'id':'bdep', 'type':"buttonSelect", 'text':'-', 'items':bdep},
                           {'type':"separator"},

                           {'type':"text", 'text':"  Тип смены:"},
                           {'id':'tbsmen', 'type':"buttonSelect", 'text':'Днев', 'items':tsmen, 'enabled':"false" if pid else "true"},

                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}, ],

                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],
                        columns:[
  { type:"ro",   sort:"str", align:"left",   width:"180", label:"Сотрудник" },
  { type:"coro", sort:"str", align:"left",   width:"*",   label:'Исполняемая роль в смене' },
  { type:"ch",   sort:"str", align:"center", width:"75",  label:"В смене" }
                        ]});
                        var combo = sw_grid.getCombo(1);                                               
                        var cmb = [%s];
                        for(var i in cmb) combo.put(cmb[i][0],cmb[i][1]);

                        window.Cleaner.push(sw_grid);
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid) }
                        
                        window.ids=%s;  //tsmen
                        window.ids2=%s; //depart
                        window.ids3=%s; //period (pid)
                                        
                        //save
                        window.do_tool_1 = function(){
                            sw_grid.editStop();
                            var dat="tsmen="+window.ids+"&period="+window.ids3;
                            
                            sw_grid.forEachRow(function(ids2){
                                if(!parseInt(sw_grid.cells(ids2, 2).getValue())){
                                    dat=dat+"&"+ids2+"=0";
                                }else{
                                    dat=dat+"&"+ids2+"="+parseInt(sw_grid.cells(ids2, 1).getValue());
                                }
                            });
                                                  
                            
                            
                              self.NetSendAsync("/personnel/openday/data", dat,function(resp) {
                                    
                                self.LoadGrid(sw_grid, "/personnel/openday/data?period="+window.ids3+"&depart="+window.ids2);  

                             });
                                                            
                        }

                        //tsmen
                        window.do_tool_2 = function(ids){
                            window.ids=ids.substr(5);
                            var text = self.Toolbars["def"].getListOptionText("tbsmen", ids);                                            
                            self.Toolbars["def"].setItemText("tbsmen", text);
                            self.Toolbars["def"].setListOptionSelected("tbsmen", ids);
                        }
                        window.do_tool_2("tsmen"+window.ids); 
                        
                        //depart
                        window.do_tool_3 = function(ids2){
                            window.ids2=ids2.substr(3);
                            var text = self.Toolbars["def"].getListOptionText("bdep", ids2);                                           
                            self.Toolbars["def"].setItemText("bdep", text);                            
                            self.LoadGrid(sw_grid, "/personnel/openday/data?period="+window.ids3+"&depart="+window.ids2);
                        }
                        self.SetTitle("%s");
                        window.do_tool_3("dep"+window.ids2);''' % (rols, pts, deps[0].id, pid, pids),
                    })

#==============================================================================
class DayDataHandler(BaseHandler):
    urls = r'/personnel/openday/data'

    def get(self):

        
        depart = self.get_argument("depart", None)
        period = self.get_argument("period", 0)

        sql = '''SELECT s.ID, s.NAME,
                        CASE
                          WHEN s.role = 1 THEN rs.NAME
                          WHEN h.ROLE IS NOT NULL THEN rh.NAME
                          ELSE rs.NAME
                        END inrole,
                        CASE
                          WHEN h.ROLE_BEGIN IS NOT NULL AND h.ROLE_END IS NULL THEN 1
                          ELSE 0
                        END insmen
                 FROM sotrud s
                 LEFT JOIN sw_role_history h ON s.id = h.SOTRUD AND h.period = :period AND h.ROLE_END IS NULL
                 LEFT JOIN sw_roles rh ON h.role = rh.id
                 LEFT JOIN sw_roles rs ON s.role = rs.id
                 WHERE s.DEPART = :depart AND s.VISIBLE = 1
                 ORDER BY 4 DESC, 3, 1'''


        self.write_XML(Executor.exec_cls(sql, period=period, depart=depart)
                       .as_grid('name', 'inrole', 'insmen', id='id'))


    def post(self):
        # TODO: добавить оповещение о смене роли ->
        # msg = {'TYPE':'W', 'TEXT': 'Роль измененена. Повторите процедуру входа'}
        # self.application.sessions.add_message(uid, True, msg)
        # self.application.sessions.add_message(uid, False, msg)

        inp = self.input(period=0, tsmen=0)

        try:
            period = int(inp.period)
            del inp['period']
            tsmena = int(inp.tsmen)
            del inp['tsmen']

            if not period:
                p = Period()
                p.tsmena = tsmena
                p.save()
                period = p.id

                x = RoleHistory()
                x.sotrud = self.session.sid
                x.period = period
                x.role = 5
                x.save()
            else:
                p = Period.get(id=period)
                if p.tsmena <> tsmena:
                    p.tsmena = tsmena
                    p.save()

            # явно подключаем начальника смены.
            # защита от роли Администратор и случайного удаления Начальника смены
            sql = 'SELECT count(*) cn FROM sw_role_history WHERE role=5 AND period = :period'
            if not Executor.exec_cls(sql, multi=False, period=p.id).cn:
                inp[str(self.session.uid)] = '5'

            nir = []  # юзеры не в смене
            for user_id, role_id in inp.items():                
                
                try: user_id = int(user_id)
                except ValueError: continue                

                try: role_id = int(role_id)
                except ValueError:
                    try:
                        role_id = User.get(id=user_id).current_role_cls.id
                    except:
                        continue

                if not role_id:
                    nir.append(user_id)
                else:
                    # завершаем текущую роль в смене
                    sql = '''UPDATE sw_role_history
                             SET role_end = SYSDATE
                             WHERE role_end IS NULL
                               AND period=:period 
                               AND sotrud=:sotrud
                               AND role<>:role'''
                    Executor.exec_sql(sql, period=period, sotrud=user_id, role=role_id)

                    # добавляем юзера в смену (если еще нету там)
                    sql = '''MERGE INTO sw_role_history
                             USING DUAL ON (sotrud=:sotrud AND 
                                            period=:period AND 
                                            role_end is NULL AND 
                                            role=:role)
                             WHEN NOT matched THEN INSERT(sotrud,  period,  role_begin, role)
                                                   VALUES(:sotrud, :period, SYSDATE,   :role)'''
                    Executor.exec_sql(sql, period=period, sotrud=user_id, role=role_id)

            # выкидываем юзеров из смены
            if nir:
                sql = '''UPDATE sw_role_history
                         SET role_end = SYSDATE
                         WHERE role_end IS NULL AND sotrud IN (%s)''' % (','.join(str(i) for i in nir))
                Executor.exec_sql(sql)

            self.write({'info':'Информация сохранена'})
        except:
            self.write({'warning':'Ошибка записи'})



#==============================================================================
class CloseDayHandler(BaseHandler):
    urls = r'/personnel/closeday'

    def get(self):
        period = Period.get_last_smen()

        if not period:
            self.write({'title':'Закрытие смены', 'def':'Нет открытых смен' })
            return

        self.write({'title':'Закрытие смены:  %s' % period.date.strftime("%d.%m.%Y %H:%M:%S"),
                    'def':[{'type':"button", 'text':'Закрыть', 'img':"accept24.png", 'imgdis':"accept24g.png", 'action':'do_tool_1'},
                           {'type':"separator"},
                           {'type':"button", 'img':"excel24.png", 'imgdis':"excel24g.png", 'action':'do_tool_csv', 'title':'Сохранить в CSV'}, ],
                    'cmd':'''var sw_grid = new dhtmlXGridObject({
                        parent: window.app.Panels["def"],
                        xml:"/personnel/closeday/data?period=%s",
                        columns:[
  { type:"ro", sort:"str", align:"left", width:"150", label:"Подразделение" },
  { type:"ro", sort:"str", align:"left", width:"200", label:"Сотрудник" },
  { type:"ro", sort:"str", align:"left", width:"120", label:"Начало" },
  { type:"ro", sort:"str", align:"left", width:"120", label:"Окончание" },
  { type:"ro", sort:"str", align:"left", width:"*",   label:"Роль" }
                        ]});
                        window.Cleaner.push(sw_grid);
                        window.do_tool_csv = function(){ self.GridCSV(sw_grid) }

                        window.do_tool_1 = function(){
                            self.NetSend("/personnel/closeday/data", "period=%s");
                            self.MakeContent("/personnel/closeday");                                
                        }
                        ''' % (period.id, period.id,)
                    })



#==============================================================================
class CloseDayDataHandler(BaseHandler):
    urls = r'/personnel/closeday/data'

    def get(self):
        period = int(self.input().period)

        sql = '''SELECT h.id, d.name dp, s.name, h.role_begin, h.role_end, r.name role
                 FROM sw_role_history h
                 JOIN sotrud s ON h.sotrud=s.id
                 JOIN sw_roles r ON h.role=r.id
                 LEFT JOIN depart d ON s.depart=d.depart
                 WHERE h.PERIOD=:period
                 ORDER BY 2,3,4'''

        self.write_XML(Executor.exec_cls(sql, period=period)
                       .as_grid('dp', 'name', 'role_begin', 'role_end', 'role', id='id',
                                show={'role_begin':lambda val: val.strftime("%d.%m.%Y %H:%M"),
                                      'role_end':lambda val: val.strftime("%d.%m.%Y %H:%M")}))


    def post(self):
        try:
            period = int(self.input().period)

            sql = 'UPDATE sw_role_history SET role_end=SYSDATE WHERE role_end IS NULL AND period=:period '
            Executor.exec_sql(sql, period=period)

            sql = 'UPDATE period SET data_end=SYSDATE WHERE period=:period '
            Executor.exec_sql(sql, period=period)

            self.write({'info':'Информация сохранена'})
        except:
            self.write({'warning':'Ошибка записи'})
