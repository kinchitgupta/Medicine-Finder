import time
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect,url_for,session
from mylib import *

app = Flask(__name__)

app.config['UPLOAD_FOLDER']='./static/photos'

app.secret_key="831c4b4a667776e4afe3a7c8112ac16508025ada18b3fb0d508b52df93b70066"

@app.route('/',methods=['GET','POST'])
def welcome():
    if request.method == 'POST':
        mname = request.form['M1']
        cur=get_db_cursor()
        sql="Select * from medicine_store where medicine_name LIKE %s order by price"
        cur.execute(sql,('%'+mname+'%'))

        data = cur.fetchall()

        if data:
            return render_template('welcome.html',data=data)
        else:
            return render_template('welcome.html',msg="no medicine found",mname=mname)
    else:
        return render_template('welcome.html')

@app.route('/adminreg',methods=['GET','POST'])
def adminreg():
  if "usertype" in session:
      usertype = session['usertype']
      if usertype == 'admin':
            if request.method == 'POST':
                name = request.form['T1']
                address = request.form['T2']
                contact = request.form['T3']
                email = request.form['T4']
                password = request.form['T5']
                usertype = "admin"
                q1="insert into admindata values ('"+name+"','"+address+"','"+contact+"','"+email+"')"
                q2="insert into logindata values ('"+email+"','"+password+"','"+usertype+"')"

                cur=get_db_cursor()
                try:

                    cur.execute(q1)
                    n1=cur.rowcount

                    cur.execute(q2)
                    n2=cur.rowcount
                    if n1>0 and n2>0:
                        msg="Data Saved and login is created"
                    elif n1==1:
                        msg="only Data is saved"
                    elif n2==1:
                        msg="Data login is created"
                    else:
                        msg="Something went wrong"
                except pymysql.err.IntegrityError:
                    msg="Duplicate entry!! email is already registered"
                return render_template('admin_reg.html',result=msg)
            else:
                return render_template('admin_reg.html')
      else:
          return redirect(url_for('auth_error'))
  else:
      return redirect(url_for('auth_error'))

@app.route('/show_admindata')
def show_admindata():
    if "usertype" in session:
        usertype = session["usertype"]
        if usertype =='admin':
            q1="select * from admindata "
            cur=get_db_cursor()
            cur.execute(q1)
            n=cur.rowcount

            if n>0:
                records=cur.fetchall()
                return render_template('show_admindata.html',data=records)
            else:
                return render_template('show_admindata.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/medicalreg',methods=['GET','POST'])
def medicalreg():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == "admin":
            if request.method=='POST':
                Store_Name=request.form['T1']
                Owner_name = request.form['T2']
                Licence_Number = request.form['T3']
                Address = request.form['T4']
                Contact = request.form['T5']
                Email = request.form['T6']
                Password = request.form['T7']
                usertype='medical'

                q1="insert into medicaldata values('"+Store_Name+"','"+Owner_name+"','"+Licence_Number+"','"+Address+"','"+Contact+"','"+Email+"')"
                q2="insert into logindata values ('"+Email+"','"+Password+"','"+usertype+"')"

                cur=get_db_cursor()
                try:
                    cur.execute(q1)
                    n1=cur.rowcount

                    cur.execute(q2)
                    n2=cur.rowcount

                    if n1>0 and n2>0:
                        msg="Data is saved and login is created"
                    elif n1==1:
                        msg="Only Data is saved"
                    elif n2==1:
                        msg="only login is created"
                    else:
                        msg="Something went wrong"
                except pymysql.err.IntegrityError:
                    msg="Duplicate entry!! email is already registered"
                return render_template('medical_reg.html',result=msg)
            else:
                return render_template('medical_reg.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/show_medicaldata')
def show_medicaldata():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype =='admin':
            cur=get_db_cursor()
            q2="select * from medicaldata "
            cur.execute(q2)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('show_medicaldata.html',data=data)
            else:
                return render_template('show_medicaldata.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/edit_medical', methods=['GET','POST'])
def edit_medical():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method=='POST':
                edit=request.form['T1']
                sql="select * from medicaldata where email='"+edit+"'"
                cur=get_db_cursor()
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template("edit_medical.html",data=data)
                else:
                    return render_template("edit_medical.html",msg="No data found")
            else:
                return redirect(url_for("show_medicaldata"))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route ('/edit_medical1', methods=['GET','POST'])
def edit_medical1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method=='POST':
                Store_Name = request.form['T1']
                Owner_Name = request.form['T2']
                Licence_Number = request.form['T3']
                Address = request.form['T4']
                Contact = request.form['T5']
                Email = request.form['T6']
                q1="update medicaldata set store_name = '"+Store_Name+"',owner_name ='"+Owner_Name+"',medical_licence ='"+Licence_Number+"',address ='"+Address+"',contact ='"+Contact+"' where email='"+Email+"'"
                cur=get_db_cursor()
                cur.execute(q1)
                n=cur.rowcount
                if n>0:
                    msg="Data is updated"
                else:
                    msg="No data saved"
                return render_template('edit_medical1.html',msg=msg)
            else:
                return render_template('edit_medical1.html',msg="no data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/del_medical', methods=['GET','POST'])
def del_medical():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method=='POST':
                email=request.form['T2']
                cur = get_db_cursor()
                sql="select * from medicaldata where email='"+email+"'"

                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template("del_medical.html",data=data)
                else:
                    return render_template("del_medical.html",msg="No data found")
            else: #GET request
                return redirect(url_for("show_medicaldata"))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/del_medical1',methods=['GET','POST'])
def del_medical1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method=='POST':
                email=request.form['T2']
                cur = get_db_cursor()
                q1="delete from medicaldata where email='"+email+"'"
                q2="delete from logindata where email='"+email+"'"

                cur.execute(q1)
                n1=cur.rowcount
                cur.execute(q2)
                n2=cur.rowcount
                if n1>0 and n2>0:
                    return render_template('del_medical1.html', msg='data deleted')
                elif n1>0:
                    return render_template('del_medical1.html', msg='only medical data deleted')
                else:
                    return render_template('del_medical1.html', msg='only login deleted')
            else:
                return redirect (url_for('show_medicaldata'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/medicine_reg',methods=['GET','POST'])
def medicine_reg():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'medical':
            if request.method=='POST':
                medicine_name=request.form['T1']
                company=request.form['T2']
                licence_number = request.form['T3']
                medical_type = request.form['T4']
                Price = request.form['T5']
                cur=get_db_cursor()
                sql="insert into medicinedata values(0,'"+medicine_name+"','"+company+"','"+licence_number+"','"+medical_type+"',"+str(Price)+",'"+e1+"')"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    msg="Data is created"
                else:
                    msg="Data is Not created"
                return render_template('medicine_reg.html',data=msg)
            else:
                return render_template('medicine_reg.html',msg='somthing went wrong')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/show_medicine')
def show_medicine():
    if 'usertype' in session:
        usertype = session['usertype']
        e1=session["email"]
        if usertype == 'medical':
            cur=get_db_cursor()
            photo = check_photo(e1)
            q="select * from medicine_with_photo where medical_email='"+e1+"'"
            cur.execute(q)
            n=cur.rowcount

            if n>0 :
                data=cur.fetchall()
                return render_template('Show_medicine.html',data=data,photo=photo)
            else:
                return render_template('Show_medicine.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route("/rival" ,methods=['GET','POST'])
def rival():
    if 'usertype' in session:
        usertype = session['usertype']
        e1=session['email']
        if usertype == 'medical':
            mname=request.form['t2']
            cur=get_db_cursor()
            q="select * from medicinedata where medical_email !='"+e1+"' and medicine_name='"+mname+"'"
            cur.execute(q)
            n=cur.rowcount
            if n>0:
                return render_template('competition.html',data=cur.fetchall())
            else:
                return render_template('competition.html',msg="No rival found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/medicine_photo', methods=['GET','POST'])
def medicine_photo():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'medical':
            file=request.files['F1']
            medid=request.form['H3']
            if file:
                path = os.path.basename(file.filename)
                file_ext = os.path.splitext(path)[1][1:]
                filename = str(int(time.time())) + '.' + file_ext
                filename = secure_filename(filename)
                sql = "insert into medicine_photo values('" + medid + "','" + filename + "')"
                cur = get_db_cursor()
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return redirect(url_for('show_medicine'))
                else:
                    return render_template('Show_medicine.html',msg1="Fail")
            else:
                return render_template('Show_medicine.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/medicine_change_photo', methods=['GET','POST'])
def medicine_change_photo():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'medical':
            medid=request.form['H4']
            photo1 = check_photo1(medid)
            cur=get_db_cursor()
            sql="delete from medicine_photo where medicine_id ='"+medid+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo1)
                return redirect(url_for('show_medicine'))
            else:
                return render_template('Show_medicine.html',msg2="Fail")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/edit_medicines',methods=['GET','POST'])
def edit_medicines():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'medical':
            if request.method=='POST':
                s=request.form['H1']
                q="select * from medicinedata where medicine_id='"+s+"'"
                cur=get_db_cursor()
                cur.execute(q)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    return render_template('edit_medicines.html',data=data)
                else:
                    return render_template('edit_medicines.html',msg="No data found")
            else:
                return redirect(url_for('show_medicine'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/edit_medicine1',methods=['GET','POST'])
def edit_medicine1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'medical':
            if request.method=='POST':
                medicine_id = request.form['T1']
                Medicine_Name=request.form['T2']
                Company=request.form['T3']
                Licence_Number = request.form['T4']
                Medical_Type = request.form['T5']
                Price = request.form['T6']
                cur=get_db_cursor()
                sql="update medicinedata set medicine_name = '"+Medicine_Name+"',company='"+Company+"',licence_number = '"+Licence_Number+"',medicine_type = '"+Medical_Type+"',price="+str(Price)+" where medicine_id='"+medicine_id+"'"
                cur.execute(sql)
                n=cur.rowcount
                msg=""
                if n>0:
                    msg="Data is changed"
                else:
                    msg="No data is changed"
                return render_template('edit_medicine1.html',data=msg)
            else:
                return redirect(url_for('show_medicine'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/del_medicine',methods=['GET','POST'])
def del_medicine():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'medical':
            if request.method=='POST':
                s1=request.form['H2']
                cur=get_db_cursor()
                q="select * from medicinedata where medicine_id='"+s1+"'"
                cur.execute(q)
                n=cur.rowcount
                if n>0:
                    d=cur.fetchone()
                    return render_template('del_medicine.html',data=d)
                else:
                    return render_template('del_medicine.html',msg="No data found")
            else:
                return redirect(url_for('show_medicine'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/del_medicine1',methods=['GET','POST'])
def del_medicine1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'medical':
            if request.method=='POST':
                d=request.form['H2']
                sql="delete from medicinedata where medicine_id='"+d+"'"
                cur=get_db_cursor()
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    return render_template('del_medicine1.html',msg='data deleted')
                else:
                    return render_template('del_medicine1.html',msg="No data found")
            else:
                return redirect(url_for('show_medicine'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        e1=request.form['T1']
        p1=request.form['T2']
        sql="select * from logindata where email='"+e1+"' and password='"+p1+"' "
        cur=get_db_cursor()
        cur.execute(sql)
        n=cur.rowcount
        if n>0:
            data=cur.fetchone()
            ut=data[2]

            session["email"]=e1
            session["usertype"]=ut

            if ut=='admin':
               return  redirect(url_for("admin_home"))
            elif ut=='medical':
                return redirect(url_for("medical_home"))
            else:
                return render_template('Login.html',msg="try connect with owner")
        else:
            return render_template('Login.html',msg="Login Failed")
    else:
        return render_template('Login.html')

@app.route('/logout')
def logout():
    if "email" in session:
        session.pop('email',None)
        session.pop('usertype',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/auth_error')
def auth_error():
    return render_template('auth_error.html')

@app.route('/admin_home')
def admin_home():

    if "usertype" in session:
        ut=session["usertype"]
        e1=session['email']
        if ut=='admin':
            admdata = getAdmin(e1)
            photo=check_photo(e1)
            return render_template('admin_home.html',data=admdata,photo=photo)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/admin_profile_photo',methods=['GET','POST'])
def admin_profile_photo():
    if 'usertype' in session:
        usertype = session['usertype']
        e1=session['email']
        if usertype == 'admin':
            file=request.files['F1']
            if file:
                path = os.path.basename(file.filename)
                file_ext = os.path.splitext(path)[1][1:]
                filename=str(int(time.time())) + '-' + file_ext
                filename=secure_filename(filename)
                sql="insert into photos values('"+e1+"','"+filename+"')"
                cur=get_db_cursor()
                try:
                    cur.execute(sql)
                    n=cur.rowcount
                    if n>0:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                        return redirect(url_for('admin_home'))
                    else:
                        return render_template("admin_home.html",result="fail")
                except:
                    return render_template("admin_home.html",result="Duplicate")
            else:
                return redirect(url_for('admin_home'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/admin_change_profile',methods=['GET','POST'])
def admin_change_profile():
    if 'usertype' in session:
        usertype = session['usertype']
        e1=session['email']
        if usertype == 'admin':
            photo=check_photo(e1)
            cur=get_db_cursor()
            sql="delete from photos where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return redirect(url_for('admin_home'))
            else:
                return render_template("admin_home.html",data1="fail")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/medical_home')
def medical_home():
    if "usertype" in session:
        ut=session["usertype"]
        e1=session['email']
        if ut=='medical':
            mdata=getmedical(e1)
            photo=check_photo(e1)
            return render_template('medical_home.html',data = mdata,photo=photo)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/medical_profile_photo',methods=['GET','POST'])
def medical_profile_photo():
    if 'usertype' in session:
        usertype = session['usertype']
        email= session['email']
        if usertype == 'medical':
            file=request.files['F2']
            if file:
                path=os.path.basename(file.filename)
                file_ext=os.path.splitext(path)[1][1:]
                filename=str(int(time.time())) + '-' + file_ext
                filename=secure_filename(filename)
                sql="insert into photos values('"+ email +"' , '"+filename+"')"
                cur=get_db_cursor()
                try:
                    cur.execute(sql)
                    n=cur.rowcount
                    if n>0:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                        return redirect(url_for('medical_home'))
                    else:
                        return render_template("medical_home.html",result="fail")
                except:
                    return render_template("medical_home.html",result="Duplicate")
            else:
                return redirect(url_for('medical_home'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/medical_change_profile',methods=['GET','POST'])
def medical_change_profile():
    if 'usertype' in session:
        usertype = session['usertype']
        e1=session['email']
        if usertype == 'medical':
            photo=check_photo(e1)
            cur=get_db_cursor()
            sql="delete from photos where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return redirect(url_for('medical_home'))
            else:
                return render_template("medical_home.html",data2="fail")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_password_admin' ,methods=['GET','POST'])
def change_password_admin():
    if "usertype" in session:
        ut=session["usertype"]
        if ut=='admin':
           if request.method=='POST':
                e1=session['email']
                p1=request.form['T1']
                p2=request.form['T2']
                sql="update logindata set password ='"+p2+"' where email='"+e1+"' and password='"+p1+"'"
                cur=get_db_cursor()
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    msg="password changed successfully"
                else:
                    msg="Invalid old password"
                return render_template('change_password_admin.html',msg=msg)
           else:
                return render_template('change_password_admin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/change_password_medical' ,methods=['GET','POST'])
def change_password_medical():
    if "usertype" in session:
        ut=session["usertype"]
        if ut=='medical':
            if request.method=='POST':
                e1=session['email']
                p1=request.form['T1']
                p2=request.form['T2']
                sql="update logindata set password = '"+p2+"' where email='"+e1+"' and password='"+p1+"'"
                cur=get_db_cursor()
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('change_password_medical.html',msg="password changed successfully")
                else:
                    return render_template('change_password_medical.html',msg="Invalid old password")
            else:
                return render_template('change_password_medical.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/edit_admin_profile',methods=['GET','POST'])
def edit_admin_profile():
    if "usertype" in session:
        user=session["usertype"]
        e1=session['email']
        if user=='admin':
            if request.method=='POST':
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                q1 ="update admindata set name = '"+name+"',address ='"+address+"',contact ='"+contact+"' where email='"+e1+"'"

                cur = get_db_cursor()
                try:
                    cur.execute(q1)
                    n1 = cur.rowcount
                    if n1 > 0:
                        return render_template('edit_admin_profile.html', result="data is saved")
                    else:
                        return render_template('edit_admin_profile.html', result="Fail")
                except pymysql.err.IntegrityError:
                    return render_template('edit_admin_profile.html', result="Duplicate Entery")
            else:
                add=getAdmin(e1)
                return render_template('edit_admin_profile.html',data=add)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/edit_medical_profile',methods=['GET','POST'])
def edit_medical_profile():
    if "usertype" in session:
        user=session["usertype"]
        e1=session['email']
        if user=='medical':
            if request.method=='POST':
                store_name=request.form['T1']
                owner_name=request.form['T2']
                licence_number=request.form['T3']
                address=request.form['T4']
                contact=request.form['T5']

                q1="update medicaldata set store_name='"+store_name+"',owner_name='"+owner_name+"',medical_licence='"+licence_number+"',address='"+address+"',contact='"+contact+"' where email='"+e1+"'"

                cur = get_db_cursor()
                cur.execute(q1)
                n1 = cur.rowcount
                if n1 > 0:
                    result = "data saved"
                else:
                    result = "data is not save"
                return render_template('edit_medical_profile.html',result=result)

            else:
                add=getmedical(e1)
                return render_template('edit_medical_profile.html',data=add)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG','false').lower()=='true')
