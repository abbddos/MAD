from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from flask_wtf.csrf import CSRFProtect, CSRFError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
#from views import login, admin, profile, project

app = Flask(__name__)

config_json = open('config.json',)
confs = json.loads(config_json.read())

app.secret_key = confs['SecretKey']
app.config['SQLALCHEMY_DATABASE_URI'] = confs['Database-URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = confs['Mail-server']
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = confs['Email-Username']
app.config['MAIL_PASSWORD'] = confs['Email-Password']
app.config['MAIL_DEFAULT_SENDER'] = confs['Email-Username']


db = SQLAlchemy(app)
csrf = CSRFProtect(app)
mail = Mail(app)


@app.route('/')
def index():
    return "This is a fuckery"

#app.register_blueprint(login.mod)
#app.register_blueprint(admin.mod)
#app.register_blueprint(profile.mod)
#app.register_blueprint(project.mod)

