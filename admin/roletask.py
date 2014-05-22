# coding: utf-8

from core.sw_base import BaseHandler
from avtuk.avtuk_models import Role
from avtuk.executor import Executor


import os
from settings import ROOT_DIR
from tornado import template


import cx_Oracle
from core.common_tools import fetchall

#=== Привязка модулей к роли =================================================#
class RoleTaskHandler(BaseHandler):
    urls = r'/admin/roletask'

    def get(self):

        loader = template.Loader(os.path.join(ROOT_DIR, 'admin'))


        all_roles = [{"value":"%s" % i.id, "name":i.name}
                     for i in Role.select("id<>1")]

        #{'id':'brole', 'type':"buttonSelect", 'items': all_roles},



        result = loader.load("roletask.js").generate(all_roles=all_roles)


        self.write({'def':[
                           '''<table style='width:100%'>
                                <tr>
                                    <td style="width:130px;">Выберите роль:</td>
                                    <td><select style="width:300px;" id="combo_zone1"></select></td>
                                </tr>
                                <tr><td colspan="2"><div id='sw_grid1' style="width:100%; height: 500px;"></div></td></tr>
                              </table>
                           '''
                           ],

                    'cmd': result
                    })



#==============================================================================
class RoleTaskDataHandler(BaseHandler):
    urls = r'/admin/roletask/data'

    def get(self):

        role = self.get_argument("role",  default=None)

        out = self.cursor.var(cx_Oracle.CURSOR)

        res = self.proc("shiva_task.role_task_type_list", [role, out])


        all_results = fetchall(res[-1])

        self.write(all_results)




    def post(self):

        role_id   = self.get_argument("role_id",   default=None)
        task_from = self.get_argument("task_from", default=None)
        task_to   = self.get_argument("task_to",   default=None)

        res = self.proc("shiva_task.set_task_type_priority", [role_id, task_from, task_to])
        




