from flask import *
from flask_mail import *
from enterprise_pmg import app
#from APIs import EnterForms
#from  APIs import EnterpriseAPI
import os

mod = Blueprint('admin', __name__, url_prefix = '/admin')

@mod.route('/')
def admin():
    return render_template('AdminTemplates/admin.html', username = session['username'], role = session['role'])