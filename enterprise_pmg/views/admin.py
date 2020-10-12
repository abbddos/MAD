from flask import *
from flask_mail import *
from enterprise_pmg import app, mail
from enterprise_pmg.model import Admin
from enterprise_pmg.Forms import AdminForms
#from APIs import EnterForms
#from  APIs import EnterpriseAPI
import os

mod = Blueprint('admin', __name__, url_prefix = '/admin')

@mod.route('/')
def admin():
    return render_template('AdminTemplates/admin.html', username = session['username'], role = session['role'], image_file = session['ProPic'])

@mod.route('/users', methods = ['GET','POST'])
def users():
    AllUsers = Admin.Users.GetAllUsers()
    form = AdminForms.CreateUser(request.form)
    return render_template('AdminTemplates/users.html', username = session['username'], 
                            role = session['role'], image_file = session['ProPic'], 
                            allusers = AllUsers, form = form)

@mod.route('/CreateNewUser', methods = ['GET','POST'])
def CreateNewUser():
    form = AdminForms.CreateUser(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                NewUser = Admin.Users(request.form['firstname'],
                                      request.form['lastname'],
                                      request.form['position'],
                                      request.form['department'],
                                      request.form['email'],
                                      request.form['phone1'],
                                      request.form.getlist('role-check'),
                                      'Active', 'default.png')
                usrname = NewUser.UserName
                pswd, hashpass = Admin.Users.createpassword(usrname)
                msg = Message('New Enterprise Account', recipients = [str(request.form['email'])])
                msg.body = "Dear {}, \n Thank you for using Enterprise. please note that your username is: {} and your password is {}. \n It is highly recommended that you change your password as soon as possible. \n Thank you for using Enterprise.".format(str(request.form['firstname']), str(usrname), str(pswd)) 
                mail.send(msg)
                flash('New user was successfully created...', category = 'success')
                return redirect(url_for('admin.users'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('admin.users'))           
    return redirect(url_for('admin.users'))

@mod.route('/UpdateUser/<uid>', methods = ['GET','POST'])
def UpdateUser(uid):
    form = AdminForms.CreateUser(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                Admin.Users.UPDATE_ONE_USER(uid,
                                            request.form['firstname'],
                                      request.form['lastname'],
                                      request.form['position'],
                                      request.form['department'],
                                      request.form['email'],
                                      request.form['phone1'],
                                      request.form.getlist('role-check'),
                                      request.form['status'], request.form['profilepic'])
                flash('User was successfully updated...', category = 'success')
                return redirect(url_for('admin.users'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('admin.users'))
    return redirect(url_for('admin.users'))

@mod.route('/ResetPassword/<uid>')
def ResetPassword(uid):
    try:
        firstname, pswd, email = Admin.Users.RESET_PASSWORD(uid)
        msg = Message('Password reset', recipients = [str(email)])
        msg.body = "Dear {}, \n Thank you for using Enterprise. please note that your  password was reset to {}. \n It is highly recommended that you change your password as soon as possible. \n Thank you for using Enterprise.".format(str(firstname), str(pswd)) 
        mail.send(msg)
        flash('User password was successfully reset...', category = 'success')
        return redirect(url_for('admin.users'))
    except Exception as e:
        flash(str(e), category = 'fail')
        return redirect(url_for('admin.users'))
    return redirect(url_for('admin.users'))