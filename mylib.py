import os
import pymysql

def get_db_cursor():
    conn = pymysql.connect(
        host=os.environ.get('DB_HOST'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        database=os.environ.get('DB_NAME'),
        ssl={'ca': 'cal.pem'},
        cursorclass=pymysql.cursors.Cursor,
        autocommit=True
    )
    return conn.cursor()
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