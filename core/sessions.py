# coding: utf-8

import time, hashlib
import settings as config


#=============================================================================#
def uid2sid(uid, mbl):
    if not uid is None:
        return hashlib.md5("%s%s%s" % (uid, mbl, config.SHIVA_COOKIE_KEY)).hexdigest()

#=============================================================================#

class SessionManager(object):
    
    def __init__(self, uid, role, rc = None):
        
        self.uid  = uid
        self.role = role
        self.rc   = rc

    def kill(self):
        
        self = None        
        
               
        
class Session(object):
    def __init__(self, uid, mbl, session_manager, role, rc=None):
        self.uid = int(uid)
        self.mbl = mbl
        self.ses = session_manager
        
        self.role = role
        
        self.rc = rc

        self.ses.data.setdefault(uid, {})
        self.ses.data[uid].setdefault(mbl, {})
        self.ses.data[uid][mbl].setdefault('data', {})
        self.ses.data[uid][mbl]['kill'] = time.time() + config.SHIVA_LIFE_SESSION
        self.ses._cleanup()
        
        
    def __repr__(self):
        return '<Session: uid=%s mbl=%s {%s}>' % (self.uid, self.mbl, self.ses.data[self.uid][self.mbl])

    def __getitem__(self, key): 
        try:
            return self.ses.data[self.uid][self.mbl]['data'][key]
        except:
            return None

    def __setitem__(self, key, val): self.ses.data[self.uid][self.mbl]['data'][key] = val
    def __delitem__(self, key): del self.ses.data[self.uid][self.mbl]['data'][key]

    def kill(self):
        try:
            del self.ses.data[self.uid][self.mbl]
        except (KeyError, IndexError):
            pass

    def get_messages(self):

        m = self.ses.get_all_messages(self.uid, self.mbl)
        self.ses.clear_messages(self.uid, self.mbl)
        return m



    def add_message(self, **msg):
        '''msg: {'TYPE':'E', 'TEXT': data} '''
        self.ses.add_message(self.uid, self.mbl, msg)

#=============================================================================#
class Sessions(object):
    def __init__(self):
        self.data = {}
        self.time_cleanup = time.time() + config.SHIVA_LIFE_SESSION  # время следующей очистки        


    def _cleanup(self):
        """Cleanup sessions"""
        current_time = time.time()
        if current_time > self.time_cleanup:
            for uid, v1 in self.data.items():
                for mbl, v2 in v1.items():
                    if current_time > v2['kill']:
                        del self.data[uid][mbl]

            self.time_cleanup = current_time + config.SHIVA_LIFE_SESSION


    def add_message(self, uid, mbl, msg):
        '''
        добавить сообщение msg для пользователя с указанным uid
        msg: {'TYPE':'E', 'TEXT': data}
        '''
        try:
            self.data[uid][mbl]['data'].setdefault('messages', [])
            self.data[uid][mbl]['data']['messages'].append(msg)
            if len(self.data[uid][mbl]['data']['messages']) > config.SHIVA_MAX_ALARM:
                del self.data[uid][mbl]['data']['messages'][0]
            return True
        except (KeyError, IndexError):
            return False

    def get_all_messages(self, uid, mbl):
        try:
            return self.data[uid][mbl]['data']['messages']
        except (KeyError, IndexError):
            return []


    def clear_messages(self, uid, mbl):
        try:
            self.data[uid][mbl]['data']['messages'] = []
        except KeyError:
            pass


    def get_message(self, uid, mbl):
        '''
        взять самое первое сообщение
        '''
        try:
            return self.data[uid][mbl]['data']['messages'][0]
        except (KeyError, IndexError):
            return {}


    def del_message(self, uid, mbl):
        '''
        удаление самого первого сообщения
        '''
        try:
            del self.data[uid][mbl]['data']['messages'][0]
        except (KeyError, IndexError):
            pass

    '''
    def del_task_message(self, uid, mbl, task_id):
        
        #удаление всех сообщений о назначенном задании(task_id) для пользователя (uid)
    
        try:
            self.data[uid][mbl]['data'].setdefault('messages', [])
        except KeyError:
            # в этой сессии нет сообщений
            return

        # цикл по всем сообщениям пользователя, если такие там вообще есть
        for i in xrange(len(self.data[uid][mbl]['data']['messages']) - 1, -1, -1):
            if int(self.data[uid][mbl]['data']['messages'][i].get('TASK_ID', 0)) == task_id:
                del self.data[uid][mbl]['data']['messages'][i]

    
    def del_task_message_everywhere(self, task_id):
        
        #удаление сообщения о назначенном задании для ВСЕХ сессий (всех пользователей)
       
        for uid in self.data.keys():
            self.del_task_message(uid, True, task_id)
            self.del_task_message(uid, False, task_id)
    '''
       
    def get_online_users(self):
        # список UID авторизованных пользователей
        res = []
        for uid in self.data.keys():
            if len(self.data[uid]):  # потому что сессия до конца не убивается...
                res.append(uid)

        return res


    def set_mbl_state(self, uid, state):
        '''
        Сохранить состояние ТСД в сессию
        '''
        self.data[uid][True]['data']['state'] = state


    def get_mbl_state(self, uid):
        '''
        Взять состояние ТСД из сессии
        '''
        try:
            return self.data[uid][True]['data']['state']
        except (KeyError, IndexError):
            return {}
