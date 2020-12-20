from flask import *
from flask_mail import *
from enterprise_pmg import app, mail
from enterprise_pmg.model import Project, Admin
from enterprise_pmg.Forms import ProjectForms
import os
from werkzeug.utils import secure_filename
from PIL import Image

mod = Blueprint('projects', __name__, url_prefix = '/projects')

@mod.route('/')
def projects():
    projs = Project.Project.GetAllProjects()
    form = ProjectForms.ProjectForm(request.form)
    users = Admin.Users.GetAllUsers()
    return render_template('ProjectTemplates/projects_home.html', username = session['username'], role = session['role'], image_file = session['ProPic'],
                            form = form,
                            projs = projs,
                            users = users)

