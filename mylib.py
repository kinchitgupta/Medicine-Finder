import pymysql
def get_db_cursor():
    cn=pymysql.connect(
        host='localhost',
        user='root',
        password='',
        port=3306,
        database='medical_store',
        autocommit=True,
    )
    cur=cn.cursor()
    return cur
def getAdmin(email):
    cur = get_db_cursor()
    sql="select * from admindata where email='%s'" % email
    cur.execute(sql)
    n=cur.rowcount
    data=None
    if n==1:
        data=cur.fetchone()
    return data

def getmedical(email):
    cur = get_db_cursor()
    sql="select * from medicaldata where email ='%s' " % email
    cur.execute(sql)
    n=cur.rowcount
    n2=None
    if n==1:
        n2= cur.fetchone()
    return n2
def check_photo(email):
    cur=get_db_cursor()
    sql="select * from photos where email = '"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    photo="no"
    if n==1:
        data=cur.fetchone()
        photo=data[1] # file in index
    return photo


def check_photo1(medicine_id):
    cur=get_db_cursor()
    sql="select * from medicine_photo where medicine_id = '"+medicine_id+"'"
    cur.execute(sql)
    n=cur.rowcount
    photo1="no"
    if n==1:
        data=cur.fetchone()
        photo1=data[1] # file in index
    return photo1