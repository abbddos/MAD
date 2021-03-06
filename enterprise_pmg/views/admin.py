from flask import *
from flask_mail import *
from enterprise_pmg import app, mail
from enterprise_pmg.model import Admin
from enterprise_pmg.Forms import AdminForms
#from APIs import EnterForms
#from  APIs import EnterpriseAPI
import os
from werkzeug.utils import secure_filename
from PIL import Image


mod = Blueprint('admin', __name__, url_prefix = '/admin')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@mod.route('/StakeHolders', methods = ['GET','POST'])
def StakeHolders():
    form = AdminForms.StakeHolderForm(request.form)
    AllStakeHolders = Admin.StakeHolder.GetAllStakeHolders()
    return render_template('AdminTemplates/stakeholders.html', username = session['username'], role = session['role'], image_file = session['ProPic'],
                            form = form, AllStakeHolders = AllStakeHolders)


@mod.route('/CreateNewStakeHolder', methods = ['GET','POST'])
def CreateNewStakeHolder():
    form = AdminForms.StakeHolderForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                Admin.StakeHolder(request.form['StakeHolderName'],
                                    request.form['StakeHolderType'],
                                    request.form['StakeHolderAddress'],
                                    request.form['StakeHolderContact'],
                                    request.form['StakeHolderEmail'],
                                    request.form['StakeHolderStatus'],
                                    request.form['StakeHolderDescription']) 
                flash('New Stake Holder was successfully created...', category = 'success')
                return redirect(url_for('admin.StakeHolders'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('admin.StakeHolders'))
    return redirect(url_for('admin.StakeHolders'))

@mod.route('/EditStakeHolder/<sid>', methods = ['GET','POST'])
def EditStakeHolder(sid):
    form = AdminForms.StakeHolderForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                Admin.StakeHolder.UpdateStakeHolder(sid, request.form['StakeHolderName'],
                                    request.form['StakeHolderType'],
                                    request.form['StakeHolderAddress'],
                                    request.form['StakeHolderContact'],
                                    request.form['StakeHolderEmail'],
                                    request.form['StakeHolderStatus'],
                                    request.form['StakeHolderDescription'])
                flash('Stake Holder information were successfully updated...', category = 'success')
                return redirect(url_for('admin.StakeHolders')) 
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('admin.StakeHolders'))
    return redirect(url_for('admin.StakeHolders'))

@mod.route('/CompanyProfile', methods = ['GET','POST'])
def CompanyProfile():
    form = AdminForms.CompanyProfileForm(request.form)
    cmp = Admin.CompanyProfile.GetCompanyByID(1)
    filename = cmp.Logo
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                file = request.files['Logo']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    out_size = (125,125)
                    i = Image.open(file)
                    i.thumbnail(out_size)
                    i.save(os.path.join(app.root_path , 'static/images/company', filename))
                Admin.CompanyProfile.UpdateCompanyProfile(
                    request.form['CompanyName'],
                    request.form['Address'],
                    request.form['Phone_1'],
                    request.form['Phone_2'],
                    request.form['Email'],
                    request.form['POBox'],
                    request.form['Registration'],
                    request.form['Description'],
                    filename
                )
                flash('Company profile was updated successfully...', category = 'success')
                return redirect(url_for('admin.CompanyProfile'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('admin.CompanyProfile'))
    return render_template('AdminTemplates/company.html', username = session['username'], role = session['role'], image_file = session['ProPic'],
                            form = form)