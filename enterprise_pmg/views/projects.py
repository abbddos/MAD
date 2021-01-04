from flask import *
from flask_mail import *
from enterprise_pmg import app, mail
from enterprise_pmg.model import Project, Admin
from enterprise_pmg.Forms import ProjectForms
import os
from werkzeug.utils import secure_filename
import datetime
from PIL import Image

mod = Blueprint('projects', __name__, url_prefix = '/projects')

@mod.route('/')
def projects():
    projs = Project.Project.GetAllProjects()
    form = ProjectForms.ProjectForm(request.form)
    users = Admin.Users.GetAllUsers()
    shs = Admin.StakeHolder.GetAllStakeHolders()
    return render_template('ProjectTemplates/projects_home.html', username = session['username'], role = session['role'], image_file = session['ProPic'],
                            form = form,
                            projs = projs,
                            users = users,
                            shs = shs)

@mod.route('/CreateProject', methods = ['GET','POST'])
def CreateProject():
    form = ProjectForms.ProjectForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                managers = request.form['Managers'].split(',')
                stakeholders = request.form['StakeHolders'].split(',')
                NewProject = Project.Project(request.form['ProjectCode'],
                                                request.form['ProjectStartDate'], 
                                                request.form['ProjectEndDate'], 
                                                request.form['Location'],
                                                request.form['FundingSource'],
                                                request.form['TotalBudget'],
                                                request.form['Currency'],
                                                managers, stakeholders,
                                                request.form['Description'], '')
                flash('New project was successfully created...', category = 'success')
                return redirect(url_for('projects.projects'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('projects.projects'))
    return redirect(url_for('projects.projects'))

@mod.route('/UpdateProject/<code>', methods = ['GET','POST'])
def UpdateProject(code):
    form = ProjectForms.ProjectForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                if request.form['Managers'] == None or request.form['ProjectStartDate'] == None or request.form['ProjectEndDate'] == None:
                    flash('Missing required values, please recheck...', category = 'fail')
                    return redirect(url_for('projects.projects'))
                else:
                    managers = request.form['Managers'].split(',')
                    stakeholders = request.form['StakeHolders'].split(',')
                    Project.Project.UpdateProjectByCode(code,
                                                request.form['ProjectStartDate'],
                                                request.form['ProjectEndDate'],
                                                request.form['Location'],
                                                request.form['FundingSource'],
                                                request.form['TotalBudget'],
                                                request.form['Currency'],
                                                managers, stakeholders,
                                                request.form['Description'],
                                                request.form['Log'])
                    flash('Project {} was successfully updated'.format(code), category = 'success')
                    return redirect(url_for('projects.projects'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('projects.projects'))
    return redirect(url_for('projects.projects'))

