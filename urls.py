from admin.chpassw import ChangePasswHandler
from admin.clearcach import AdminClearCachDataHandler
from admin.clearcach import AdminClearCachHandler
from admin.edirepo import AdminEdiRepoDataHandler
from admin.edirepo import AdminEdiRepoHandler
from admin.rawsql import RawSQLDATAHandler
from admin.rawsql import RawSQLHandler
from admin.rolemod import AdminDataHandler
from admin.rolemod import RoleModuleHandler


from admin.roletask import RoleTaskHandler
from admin.roletask import RoleTaskDataHandler



from admin.sys import SysStatDataHandler
from admin.sys import SysStatDataHandlerStatus
from admin.sys import SysStatHandler
from admin.testpro import AdminTestproDataHandler
from admin.testpro import AdminTestproHandler

from btk.blockl import BTKBlockDataHandler
from btk.blockl import BTKBlockHandler
from btk.chkbtk import BTKChkDataHandler
from btk.chkbtk import BTKChkHandler


from btk.btkconfirmin import BTKConfirmIn, BTKConfirmInData


from core.auth import AuthHandler
from core.auth import LogoutHandler

from core.index import MainHandler
from core.menu import MenuHandler
from core.system import SystemCSVHandler
from core.system import SystemHelpHandler
from core.system import SystemMessageHandler

from group.boxass import BoxAssembleDataHandler
from group.boxass import BoxAssembleHandler

from itemzone.itemassembly import ItemAssemblyDataHandler
from itemzone.itemassembly import ItemAssemblyHandler
from itemzone.itempackage import ItemzoneItempackageDataHandler
from itemzone.itempackage import ItemzoneItempackageHandler

from mbl.acception import AcceptionHandler
from mbl.acception import ItemListHandler
from mbl.manual import InventoryHandler
from mbl.manual import ManualIncrease
from mbl.manual import ManualValidation
from mbl.mbl import AllocationHandler
from mbl.mbl import BatchingOrders
from mbl.mbl import CellFail
from mbl.mbl import TaskHandler
from mbl.mbl import MovingHandler



from personnel.alltsk import AllTaskDataHandler
from personnel.alltsk import AllTaskHandler
from personnel.currtsk import CurrentTaskHandler
from personnel.epersonnel import EditUserDataHandler
from personnel.epersonnel import EditUserHandler
from personnel.openday import CloseDayDataHandler
from personnel.openday import CloseDayHandler
from personnel.openday import DayDataHandler
from personnel.openday import OpenDayHandler
from personnel.personnel import PersonnelDataHandler
from personnel.personnel import PersonnelHandler
from personnel.prnuser import PrintUserDataHandler
from personnel.prnuser import PrintUserHandler
from personnel.roleoper import RoleDefaultDataHandler
from personnel.roleoper import RoleDefaultHandler

from revision.blockcell import BlockCellDataHandler
from revision.blockcell import BlockCellHandler

from revision.auditor import AuditorDataHandler
from revision.auditor import AuditorHandler

from revision.saldo_gap import Saldo_GapDataHandler
from revision.saldo_gap import Saldo_GapHandler

from revision.change_party import Change_party
from revision.change_party import Change_party_data




from warehouse.acceptance import AcceptanceDataHandler
from warehouse.acceptance import AcceptanceHandler
from warehouse.assembly import AssemblyDataHandler
from warehouse.assembly import AssemblyHandler
from warehouse.printpassport import PrintPassportDataHandler
from warehouse.printpassport import PrintPassportHandler
from warehouse.prncell import PrintCellDataHandler
from warehouse.prncell import PrintCellHandler
from warehouse.prnpalet import PrintPalletDataHandler
from warehouse.prnpalet import PrintPalletHandler
from warehouse.prnpart import PrintParDataHandler
from warehouse.prnpart import PrintPartHandler
from warehouse.prnpartreg import PrintPartRegDataHandler
from warehouse.prnpartreg import PrintPartRegHandler
from warehouse.wareaddr import WareAddressDataHandler
from warehouse.wareaddr import WareAddressHandler


from warehouse.sborka import SborkaDataHandler
from warehouse.sborka import SborkaHandler


from expimp.exportcell import ExportCellHandler, ExportCellDataHandler
from expimp.importtovar import ImportTovarHandler
# from expimp.create_tovar import CreateTovarHandler


from mbl.sborka import Terminal_Sborka


from tornado import web
from settings import STATIC_DIR

handlers = [
                (r"/static/(.*)", web.StaticFileHandler, {"path":  STATIC_DIR}),
                (r"/", MainHandler),
                (r"/restart", MainHandler),
                (r"/admin/chpassw", ChangePasswHandler),
                (r"/admin/clearcach", AdminClearCachHandler),
                (r"/admin/clearcach/data", AdminClearCachDataHandler),
                (r"/admin/edirepo", AdminEdiRepoHandler),
                (r"/admin/edirepo/data", AdminEdiRepoDataHandler),
                (r"/admin/rawsql", RawSQLHandler),
                (r"/admin/rawsql/data", RawSQLDATAHandler),
                (r"/admin/rolemod", RoleModuleHandler),
                (r"/admin/rolemod/data", AdminDataHandler),

                (r"/admin/roletask",      RoleTaskHandler),
                (r"/admin/roletask/data", RoleTaskDataHandler),

                (r"/admin/sys", SysStatHandler),
                (r"/admin/sys/data", SysStatDataHandler),
                (r"/admin/sys/status", SysStatDataHandlerStatus),
                (r"/admin/testpro", AdminTestproHandler),
                (r"/admin/testpro/data", AdminTestproDataHandler),
                (r"/auth", AuthHandler),
                (r"/btk/blockl", BTKBlockHandler),
                (r"/btk/blockl/data", BTKBlockDataHandler),
                (r"/btk/chkbtk", BTKChkHandler),
                (r"/btk/chkbtk/data/([^/]+)", BTKChkDataHandler),
                
                (r"/btk/btkconfirmin", BTKConfirmIn),
                (r"/btk/btkconfirmin/data/([^/]+)", BTKConfirmInData),
                
                
                (r"/group/boxass", BoxAssembleHandler),
                (r"/group/boxass/data", BoxAssembleDataHandler),
                (r"/itemzone/itemassembly", ItemAssemblyHandler),
                (r"/itemzone/itemassembly/data", ItemAssemblyDataHandler),
                (r"/itemzone/itempackage", ItemzoneItempackageHandler),
                (r"/itemzone/itempackage/data", ItemzoneItempackageDataHandler),
                (r"/logout", LogoutHandler),
                (r"/n", MainHandler),
                
                        
                (r"/task/(.*)", TaskHandler),
                (r"/mbl/moving/(.*)", MovingHandler),
                (r"/mbl/alloc/(.*)", AllocationHandler),
                                
                (r"/mbl/acception/(.*)", AcceptionHandler),
          
                (r"/mbl/batching/(.*)", BatchingOrders),
                (r"/mbl/fail", CellFail),
                
                (r"/mbl/increase/([^/]+)", ManualIncrease),
                (r"/mbl/inventory/([^/]+)", InventoryHandler),
                
                (r"/warehouse/prnpart", PrintPartHandler),
                (r"/warehouse/prnpart/data/(.*)", PrintParDataHandler),
                
                
                (r"/mbl/items", ItemListHandler),
                
                (r"/mbl/valid", ManualValidation),
                
                (r"/sborka/(.*)", Terminal_Sborka),
                
                (r"/menu", MenuHandler),
                (r"/personnel/alltsk", AllTaskHandler),
                (r"/personnel/alltsk/data/(.*)", AllTaskDataHandler),
                (r"/personnel/currtsk", CurrentTaskHandler),
                
                
                (r"/personnel/closeday", CloseDayHandler),
                (r"/personnel/closeday/data", CloseDayDataHandler),
                
                
                
                (r"/personnel/epersonnel", EditUserHandler),
                (r"/personnel/epersonnel/data", EditUserDataHandler),
                (r"/personnel/openday", OpenDayHandler),
                (r"/personnel/openday/data", DayDataHandler),
                (r"/personnel/personnel", PersonnelHandler),
                (r"/personnel/personnel/data", PersonnelDataHandler),
                (r"/personnel/prnuser", PrintUserHandler),
                (r"/personnel/prnuser/data", PrintUserDataHandler),
                (r"/personnel/roleoper", RoleDefaultHandler),
                (r"/personnel/roleoper/data", RoleDefaultDataHandler),
                
                (r"/revision/blockcell", BlockCellHandler),
                (r"/revision/blockcell/data/([^/]+)", BlockCellDataHandler),
                (r"/revision/auditor", AuditorHandler),
                (r"/revision/auditor/data/([^/]+)", AuditorDataHandler),
                
                (r"/revision/saldo_gap", Saldo_GapHandler),
                (r"/revision/saldo_gap/data/([^/]+)", Saldo_GapDataHandler),
                
                (r"/revision/change_party", Change_party),
                (r"/revision/change_party/data/([^/]+)", Change_party_data),                
                
                
                (r"/system/csv", SystemCSVHandler),
                (r"/system/help/(.*)", SystemHelpHandler),
                (r"/system/message", SystemMessageHandler),
                (r"/warehouse/acceptance", AcceptanceHandler),
                (r"/warehouse/acceptance/data/([^/]+)", AcceptanceDataHandler),
                (r"/warehouse/assembly", AssemblyHandler),
                (r"/warehouse/assembly/data/([^/]+)", AssemblyDataHandler),
                (r"/warehouse/printpassport", PrintPassportHandler),
                (r"/warehouse/printpassport/data/([^/]+)", PrintPassportDataHandler),
                (r"/warehouse/prncell", PrintCellHandler),
                (r"/warehouse/prncell/data", PrintCellDataHandler),
                (r"/warehouse/prnpalet", PrintPalletHandler),
                (r"/warehouse/prnpalet/data", PrintPalletDataHandler),
                
                
                
                (r"/warehouse/sborka", SborkaHandler),
                (r"/warehouse/sborka/data/([^/]+)", SborkaDataHandler),            
                
                (r"/warehouse/prnpartreg", PrintPartRegHandler),
                (r"/warehouse/prnpartreg/data", PrintPartRegDataHandler),
                (r"/warehouse/wareaddr", WareAddressHandler),
                (r"/warehouse/wareaddr/data", WareAddressDataHandler),
                
                (r"/expimp/exportcell", ExportCellHandler),
                (r"/expimp/exportcell/data", ExportCellDataHandler),
                
                (r"/expimp/importtovar", ImportTovarHandler),
               # (r"/expimp/create_tovar",  CreateTovarHandler),

        ]    
