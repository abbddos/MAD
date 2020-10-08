
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from flask_wtf.csrf import CSRFProtect, CSRFError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
from enterprise_pmg.model import Admin
from enterprise_pmg import app
from enterprise_pmg.Forms import LoginForms


def ForgotPasswordToken(email):
    con, cur = root()
    try:
        cur.execute("SELECT firstname, username FROM users WHERE email = %s ", (email,))
        usr = cur.fetchone()
        con.close()

        s = Serializer(app.secret_key, 1800)
        token = s.dumps({'user':usr[1]}).decode('utf-8')
        return usr, token
    except:
        con.close()
        return None, None

def VerifyToken(token):
    s = Serializer(app.secret_key)
    try:
        usr = s.loads(token)['user']
    except:
        return None
    return usr


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForms.LoginForm(request.form)
    if request.method == 'POST':
        #try:
        if request.form['submit'] == 'Login' and form.validate():
            username = request.form['usrname']
            passwd = request.form['passwd']
            logger = Admin.Users.LOGGER(username, passwd)
            if logger['Logged'] == True:
                session['username'] = logger['username']
                #session['password'] = logger['password']
                session['role'] = logger['role']
                return redirect(url_for('home'))
            elif logger['Logged'] == False:
                flash('LOGIN ERROR: Bad username or password', category = 'fail')
                return render_template('LoginTemplates/login.html', form = form)
        #except:
        #    flash('LOGIN ERROR: Bad username or password', category = 'fail')
        #    return render_template('LoginTemplates/login.html', form = form)

    return render_template('LoginTemplates/login.html', form = form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/forgot_password', methods = ['GET','POST'])
def ForgotPassword():
    form = LoginForms.ForgotPassword(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                usr, token = ForgotPasswordToken(request.form['email'])
                if token is not None:
                    msg = Message('New Enterprise Account', recipients = [str(request.form['email'])])
                    msg.body = "Dear {}:\n please follow the link below to change your password. \n Thank you for using Enterprise. \n {}".format(usr[0], url_for('ChangeForgotPassword', usr = usr[1], token = token, _external=True))
                    mail.send(msg)
                    flash('An email was sent to your email account', category = 'success')
                    return redirect(url_for('ForgotPassword'))
                else:
                    flash('Email not found', category = 'fail')
                    return redirect(url_for('ForgotPassword'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('ForgotPassword'))
    return render_template('LoginTemplates/forgot_password.html', form = form)

@app.route('/change_forgot_password/<token>', methods = ['GET','POST'])
def ChangeForgotPassword(token):
    form = LoginForms.ChangePassword(request.form)
    usr = VerifyToken(token)
    if usr:
        if request.method == 'POST':
            if request.form['submit'] == 'Submit' and request.form['newpswd'] == request.form['confirm']:
                try:
                    ChangePassword1(usr, request.form['newpswd'])
                    flash('Password changed...', category = 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    flash(str(e), category = 'fail')
                    return redirect(url_for('login'))
        return render_template('LoginTemplates/change_forgot_password.html', form = form, token = token)
    else:
        return render_template('LoginTemplates/invalid_token.html')

@app.route('/home')
def home():
    return render_template('LoginTemplates/home.html', username = session['username'], role = session['role'] )



