from flask import *
from flask_mail import *
from enterprise_pmg import app, mail
from enterprise_pmg.model import Projects, Admin
from enterprise_pmg.Forms import ProjectForms
import os
from werkzeug.utils import secure_filename
import datetime
from PIL import Image

mod = Blueprint('projects', __name__, url_prefix = '/projects')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_document(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS

def CheckManagers(ManagersList):
    allunames = Admin.Users.GetAllUserNames()
    for m in ManagersList:
        if m not in allunames:
            return '{} is not included as a user'.format(m)
            break
    return None

def CheckStakeHolders(stakeholderslist):
    allnames = Admin.StakeHolder.GetStakeHoldersList()
    for s in stakeholderslist:
        if s not in allnames:
            return 'Stakeholder {} is not identified.'.format(s)
            break
    return None

def GetProjectImages(code):
    return os.listdir(app.root_path + "/static/projects/{}/images".format(code))

def GetProjectDocs(code):
    return os.listdir(app.root_path + "/static/projects/{}/documents".format(code))
    

def CreateProjectDirectory(code):
    os.mkdir(app.root_path + "/static/projects/{}".format(code))
    os.mkdir(app.root_path + "/static/projects/{}/documents".format(code))
    os.mkdir(app.root_path + "/static/projects/{}/images".format(code))

    
@mod.route('/')
def projects():
    return redirect(url_for('projects.allprojects'))

@mod.route('/allprojects', methods = ['Get','POST'])
def allprojects():
    projs = Projects.Project.GetAllProjects()
    form = ProjectForms.ProjectForm(request.form)
    users = Admin.Users.SELECT_ALL()
    shs = Admin.StakeHolder.GET_ALL_STAKEHOLDERS()
    return render_template('ProjectTemplates/projects_home.html', username = session['username'], role = session['role'], image_file = session['ProPic'],
                            form = form,
                            allprojects = projs,
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
                mancheck = CheckManagers(managers)
                shcheck = CheckStakeHolders(stakeholders)
                if mancheck:
                    flash(mancheck, category = 'fail')
                    return redirect(url_for('projects.allprojects'))
                elif shcheck:
                    flash(shcheck, category = 'fail')
                    return redirect(url_for('projects.allprojects'))
                else:
                    NewProject = Projects.Project(request.form['ProjectCode'],
                                                request.form['ProjectStartDate'], 
                                                request.form['ProjectEndDate'], 
                                                request.form['Location'],
                                                request.form['FundingSource'],
                                                request.form['TotalBudget'],
                                                request.form['Currency'],
                                                managers, stakeholders,
                                                request.form['Description'], request.form['Log'])
                    CreateProjectDirectory(request.form['ProjectCode'])
                    flash('New project was successfully created...', category = 'success')
                    return redirect(url_for('projects.allprojects'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('projects.allprojects'))
    return redirect(url_for('projects.allprojects'))

@mod.route('/UpdateProject/<code>', methods = ['GET','POST'])
def UpdateProject(code):
    form = ProjectForms.ProjectForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                if request.form['Managers'] == None or request.form['ProjectStartDate'] == None or request.form['ProjectEndDate'] == None:
                    flash('Missing required values, please recheck...', category = 'fail')
                    return redirect(url_for('projects.allprojects'))
                else:
                    managers = request.form['Managers'].split(',')
                    stakeholders = request.form['StakeHolders'].split(',')
                    mancheck = CheckManagers(managers)
                    shcheck = CheckStakeHolders(stakeholders)
                    if mancheck:
                        flash(mancheck, category = 'fail')
                        return redirect(url_for('projects.allprojects'))
                    elif shcheck:
                        flash(shcheck, category = 'fail')
                        return redirect(url_for('projects.allprojects'))
                    else:
                        Projects.Project.UpdateProjectByCode(code,
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
                        return redirect(url_for('projects.allprojects'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('projects.allprojects'))
    return redirect(url_for('projects.allprojects'))

@mod.route('/project/<code>', methods = ['GET','POST'])
def project(code):
    imgs = GetProjectImages(code)
    docs = GetProjectDocs(code)
    TaskForm = ProjectForms.TaskForm(request.form)
    return render_template('ProjectTemplates/project.html', username = session['username'], role = session['role'], image_file = session['ProPic'], code = code,
    imgs = imgs, docs = docs, 
    TaskForm = TaskForm)

@mod.route('/uploadfiles/<code>', methods = ['Get','POST'])
def UploadFiles(code):
    if request.method == 'POST':
        try:
            files = request.files.getlist('file')
            for file in files:
                if file and allowed_document(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.root_path , 'static/projects/{}/documents'.format(code), filename))
            return redirect(url_for('projects.project', code = code))
        except Exception as e:
            flash(str(e), category = 'fail')
            return redirect(url_for('projects.project', code = code))
    return redirect(url_for('projects.project', code = code))

@mod.route('/removefile/<code>/<file>')
def RemoveFile(code, file):
    os.remove(app.root_path + '/static/projects/{}/documents/{}'.format(code, file))
    return redirect(url_for('projects.project', code = code))

@mod.route('/removeimage/<code>/<file>')
def RemoveImage(code, file):
    os.remove(app.root_path + '/static/projects/{}/images/{}'.format(code, file))
    return redirect(url_for('projects.project', code = code))


@mod.route('/uploadimages/<code>', methods = ['GET','POST'])
def UploadImages(code):
    if request.method == 'POST':
        try:
            files = request.files.getlist('file')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.root_path , 'static/projects/{}/images'.format(code), filename))
            return redirect(url_for('projects.project', code = code))
        except Exception as e:
            flash(str(e), category = 'fail')
            return redirect(url_for('projects.project', code = code))
    return redirect(url_for('projects.project', code = code))

