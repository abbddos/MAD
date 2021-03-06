from flask_wtf import *
from flask_wtf.file import FileField, FileAllowed
from wtforms import *
from wtforms.validators import *

class LoginForm(Form):
    usrname = StringField('Username: ', validators = [DataRequired()])
    passwd = PasswordField('Password: ', validators = [DataRequired()])

class ForgotPassword(Form):
    email = StringField('Email', validators = [DataRequired()])

class ChangeForgotPassword(Form):
    NewPassword = PasswordField('New Password: ', validators = [DataRequired()])
    ConfirmNewPassword = PasswordField('Conform New Password: ', validators = [DataRequired()])
    submit = SubmitField('Submit')