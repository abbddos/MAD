from flask_wtf import *
from flask_wtf.file import FileField, FileAllowed
from wtforms import *
from wtforms.validators import *

class CreateUser(Form):
    firstname = StringField('First Name: ', validators = [DataRequired('This field is required')])
    lastname = StringField('Last Name: ', validators = [DataRequired('This field is required')])
    position = StringField('Position: ')
    department = StringField('Department: ')
    email = StringField('Email: ', validators = [DataRequired('This field is required'), Email()])
    phone1 = StringField('Phone #1: ')
    submit = SubmitField('Submit')

class CompanyProfileForm(Form):
    CompanyName = StringField('Company Name: ', validators = [DataRequired('This field is required')])
    Address = StringField('Address: ')
    Phone_1 = StringField('Phone #1: ')
    Phone_2 = StringField('Phone #2: ')
    Email = StringField('Email: ', validators = [Email()])
    POBox = StringField('PO-Box')
    Registration = StringField('Registration: ')
    Description = TextAreaField('Description: ')
    Logo = FileField('Logo: ', validators = [FileAllowed(['png', 'jpeg', 'jpg'])])
    submit = SubmitField('Submit')