from flask import *
from flask_mail import *
from enterprise_pmg import app, mail
from enterprise_pmg.model import Admin
from enterprise_pmg.Forms import ProfileForms
#from APIs import EnterForms
#from  APIs import EnterpriseAPI
import os
from werkzeug.utils import secure_filename
from PIL import Image

mod = Blueprint('profile', __name__, url_prefix = '/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mod.route('/')
def profile():
    return render_template('ProfileTemplates/profile.html', username = session['username'], role = session['role'], image_file = session['ProPic'])

@mod.route('/UserProfile/<uname>', methods = ['GET','POST'])
def UserProfile(uname):
    usr = Admin.Users.SELECT_ONE_USER(uname)
    uid = usr.UserId
    pos = usr.Position
    dep = usr.Department
    stat = usr.Status
    rol = usr.Role
    filename = usr.ProfilePic
    form = ProfileForms.EditUserForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                file = request.files['ProfilePic']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    out_size = (125,125)
                    i = Image.open(file)
                    i.thumbnail(out_size)
                    i.save(os.path.join(app.root_path , 'static/images/users', filename))
                Admin.Users.UPDATE_ONE_USER(uid,
                                            request.form['firstname'],
                                            request.form['lastname'],
                                            pos, dep,
                                            request.form['email'],
                                            request.form['phone1'],
                                            rol, stat, filename)
                flash('Your profile was successfully updated...', category = 'success')
                return redirect(url_for('profile.UserProfile', uname = uname))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('profile.UserProfile', uname = uname))
    return render_template('ProfileTemplates/userprofile.html', username = session['username'], role = session['role'], image_file = session['ProPic'],
                            form = form, uname = uname)

@mod.route('/ChangePassword/<uname>', methods = ['GET','POST'])
def ChangePassword(uname):
    form = ProfileForms.ChangePassword(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                if request.form['NewPassword'] != request.form['ConfirmNewPassword']:
                    flash('New password does not match confirmation...', category = 'fail')
                    return redirect(url_for('profile.ChangePassword', uname = session['username']))
                else:
                    Admin.Users.CHANGE_PASSWORD_BY_USERNAME(uname, request.form['CurrentPassword'], request.form['NewPassword'])
                    flash('Your password was successfully changed...', category = 'success')
                    return redirect(url_for('profile.ChangePassword', uname = session['username']))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('profile.ChangePassword', uname = session['username']))
    return render_template('ProfileTemplates/changepassword.html', username = session['username'], role = session['role'], image_file = session['ProPic'],
                            form = form)