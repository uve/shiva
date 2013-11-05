import os
import time
import cx_Oracle


from settings import RC_IP, RC_PORT, DB_LOGIN, DB_PASSWORD, DB_SID


# Example: Sub-optimal connection pooling with Oracle 11g DRCP and cx_Oracle

def do_connection():
    print 'Starting do_connection ' + str(os.getpid())
    
            
    dsn = cx_Oracle.makedsn(RC_IP, RC_PORT, DB_SID)
    
    mypool = cx_Oracle.SessionPool(user=DB_LOGIN,password=DB_PASSWORD,dsn=dsn,min=1,max=2,increment=1)    
    con = cx_Oracle.connect(user=DB_LOGIN, password=DB_PASSWORD,
          dsn=dsn, pool = mypool, cclass="CJDEMO3", purity=cx_Oracle.ATTR_PURITY_SELF)
    
    cur = con.cursor()
    print 'Querying ' + str(os.getpid())
    cur.execute("select to_char(systimestamp) from dual")
    print cur.fetchall()
    cur.close()
    
    mypool.release(con)
    print 'Sleeping ' + str(os.getpid())
    time.sleep(30)
    print 'Finishing do_connection ' + str(os.getpid())


#do_connection()

for x in range(100):
    pid = os.fork()
    if not pid:
        do_connection()
        os._exit(0)
