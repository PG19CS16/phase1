import datetime

from flask import Flask,request,render_template,redirect,session
from DBConnection import Db
app = Flask(__name__)
app.secret_key="abc"



@app.route('/')
def login():
    return render_template('login_index.html')


@app.route('/loginn',methods=['post'])
def loginn():
        na=request.form['u']
        pw=request.form['p']
        db=Db()
        res=db.selectOne("select * from login where username='"+na+"'and password='"+pw+"'")
        if res is not None:
            if res['usertype']=="admin":
                session['lin']='lin'
                return redirect('/admin_home')
            else:
                return '<script>alert("Invalid details!!");window.location="/"</script>'
        else:
            return '<script>alert("User not found");window.location="/"</script>'



@app.route('/admin_home')
def admin_home():
    if session['lin']=='lin':
        return render_template('admin/admin_index.html')
    else:
        return redirect('/')

@app.route('/view_user')
def view_user():
    if session['lin'] == "lin":
        db = Db()
        qry = db.select("select * from user  ")
        return render_template("admin/view_users.html", a=qry)
    else:
        return redirect('/')


@app.route('/view_complaint')
def view_complaint():
    if session['lin'] == "lin":
        db = Db()
        qry = db.select("select * from complaint,user where complaint.user_id=user.user_id ")
        return render_template("admin/view_Complaint.html", a=qry)
    else:
        return redirect('/')

@app.route('/reply/<a>')
def reply(a):
    return render_template('admin/send_reply.html',cid=a)

@app.route('/reply1/<a>', methods=['post'])
def reply1(a):
    if session['lin'] == "lin":
            db = Db()
            rply = request.form['textarea']
            qry = db.update("update complaint set reply='" + rply + "',r_date=curdate() where complaint_id='" + a + "'")
            return '<script>alert("Success");window.location="/view_complaint#aa"</script>'

    else:
        return redirect('/')

@app.route('/change_password')
def change_password():
    return render_template('admin/change_password.html')

@app.route('/change_password1', methods=['post'])
def change_password1():
    if session['lin'] == "lin":

            old_password = request.form['o']
            new_password = request.form['n']
            con_password = request.form['c']

            db = Db()
            res = db.selectOne("SELECT * FROM `login` WHERE `password` = '" + old_password + "' AND usertype = 'admin' ")
            if res is not None:
                if new_password == con_password:
                    db = Db()
                    db.update("update `login` set `password`='" + con_password + " ' where usertype = 'admin'")
                    return '''<script>alert('success');window.location="/admin_home"</script>'''
                else:
                    return '''<script>alert('Password mismatch!!');window.location="/change_password#aa"</script>'''
            else:
                return '''<script>alert('Incorrect password!!');window.location="/change_password#aa"</script>'''

    else:
        return redirect('/')

# ==============================================================================================================================
#                                         USER MODULE
# ===============================================================================================================================
@app.route('/register',methods=['get','post'])
def register():
        if request.method=="POST":
            name=request.form['n']
            place=request.form['p']
            post=request.form['po']
            pin=request.form['pi']
            contact=request.form['ph']
            email=request.form['em']
            password=request.form['ps']

            db=Db()
            qry1=db.selectOne("select * from login where username='"+email+"'")
            if qry1 is not None:
                return '''<script>alert('Email already exist!');window.location="/register"</script>'''

            else:
                qry = db.insert("insert into login VALUES ('','" + email + "','" + password + "','user')")
                db.insert("insert into user VALUES ('" + str( qry) + "','" + name + "','" + place + "','" + post + "','" + pin + "','" + email + "','"+contact+"')")
                return '''<script>alert('success');window.location="/"</script>'''
        else:
            return render_template('user/reg.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    session['lin']=""
    return redirect('/')

if __name__ == '__main__':
    app.run(port=4000)
