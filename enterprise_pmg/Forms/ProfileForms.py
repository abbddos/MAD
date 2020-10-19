from flask_wtf import *
from flask_wtf.file import FileField, FileAllowed
from wtforms import *
from wtforms.validators import *

class EditUserForm(Form):
    firstname = StringField('First Name: ', validators = [DataRequired('This field is required')])
    lastname = StringField('Last Name: ', validators = [DataRequired('This field is required')])
    position = StringField('Position: ')
    department = StringField('Department: ')
    email = StringField('Email: ', validators = [DataRequired('This field is required'), Email()])
    phone1 = StringField('Phone #1: ')
    ProfilePic = FileField('Select Profile Picture: ', validators = [FileAllowed(['png', 'jpeg', 'jpg'])])
    submit = SubmitField('Submit')

class ChangePassword(Form):
    CurrentPassword = PasswordField('Current Password: ', validators = [DataRequired()])
    NewPassword = PasswordField('New Password: ', validators = [DataRequired()])
    ConfirmNewPassword = PasswordField('Confirm New Password: ', validators = [DataRequired()])
    submit = SubmitField('Submit')

