from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_restful import Api
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json

# Building the application using Flask
app = Flask(__name__)


#loading the application configuration from config.json...
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


#Creating application APIs.
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
mail = Mail(app)
api = Api(app)

#Importing application packages
from enterprise_pmg import routes
from enterprise_pmg.views import admin, profile
from enterprise_pmg.API import AdminApi, ProjectApi 
#, profile, projects

#Connecting Modules
app.register_blueprint(admin.mod)
app.register_blueprint(profile.mod)
#app.register_blueprint(projects.mod)


#Connecting REST API...
#...Adminisration API...
api.add_resource(AdminApi.GetAllUsers, '/API/Admin/GetAllUsers')
api.add_resource(AdminApi.GetUserByID, '/API/Admin/GetUserByID/<uid>')
api.add_resource(AdminApi.GetUserByUname, '/API/Admin/GetUserByUname/<uname>')
api.add_resource(AdminApi.GetCompanyByID, '/API/Admin/GetCompanyByID/<cid>')
api.add_resource(AdminApi.GetAllStakeHolders, '/API/Admin/GetAllStakeHolders')
api.add_resource(AdminApi.GetStakeHolderByID, '/API/Admin/GetStakeHolderByID/<sid>')

#...Projects API...
api.add_resource(ProjectApi.GetAllProjects, '/API/Projects/GetAllProjects')
api.add_resource(ProjectApi.GetProjectByID, '/API/Projects/GetProjectByID/<pid>')
api.add_resource(ProjectApi.GetProjectByCode, '/API/Projects/GetProjectByCode/<code>')


