from flask_wtf import *
from flask_wtf.file import FileField, FileAllowed
from wtforms import *
from wtforms.validators import *

class CreateUser(Form):
    firstname = StringField('First Name: ', validators = [DataRequired()])
    lastname = StringField('Last Name: ', validators = [DataRequired()])
    position = StringField('Position: ')
    department = StringField('Department: ')
    email = StringField('Email: ')
    phone1 = StringField('Phone #1: ')
    