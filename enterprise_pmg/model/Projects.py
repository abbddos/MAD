from enterprise_pmg import db

class Project(db.Model):
    ProjectID = db.Column(db.Integer, primary_key = True)
    ProjectCode = db.Column(db.String(10), nullable = False, unique = True)
    StartDate = db.Column(db.Date, nullable = False)
    EndDate = db.Column(db.Date, nullable = False)
    Location = db.Column(db.String(100))
    FundingSource = db.Column(db.String(100))
    TotalBudget = db.Column(db.Float)
    Currency = db.Column(db.String(3))
    ProjectManagers = db.Column(db.ARRAY(db.String(50)), nullable = False)
    ProjectStakeHolders = db.Column(db.ARRAY(db.String(100)))
    Description = db.Column(db.Text)
    Log = db.Column(db.Text)
    tasks = db.relationship('Tasks', backref = 'project', lazy = True)

    def __init__(self, code, startdate, enddate, location, fsource, budget, currency, managers, stakeholders, description, log):
        self.ProjectCode = code
        self.StartDate = startdate
        self.EndDate = enddate
        self.Location = location
        self.FundingSource = fsource
        self.TotalBudget = budget
        self.Currency = currency
        self.ProjectManagers = managers
        self.ProjectStakeHolders = stakeholders
        self.Description = description
        self.Log = log
        db.session.add(self)
        db.session.commit()

    def GET_ALL_PROJECTS():
        qrys = Project.query.order_by(Project.ProjectID.desc()).all()
        return qrys 

    def GetAllProjects():
        qrys = Project.query.order_by(Project.ProjectID.desc()).paginate(per_page = 5)
        return qrys 

    def GetProjectByID(pid):
        qry = Project.query.filter_by(ProjectID = pid).first()
        return qry

    def GetProjectByCode(code):
        qry = Project.query.filter_by(ProjectCode = code).first()
        return qry

    def UpdateProjectByID(pid, startdate, enddate, location, fsource, budget, currency, managers, stakeholders, description, log):
        proj = Project.GetProjectByID(pid)
        proj.StartDate = startdate
        proj.EndDate = enddate
        proj.Location = location
        proj.FundingSource = fsource
        proj.TotalBudget = budget
        proj.Currency = currency
        proj.ProjectManagers = managers
        proj.ProjectStakeHolders = stakeholders
        proj.Description = description
        proj.Log = log
        db.session.commit()

    def UpdateProjectByCode(code, startdate, enddate, location, fsource, budget, currency, managers, stakeholders, description, log):
        proj = Project.GetProjectByCode(code)
        proj.StartDate = startdate
        proj.EndDate = enddate
        proj.Location = location
        proj.FundingSource = fsource
        proj.TotalBudget = budget
        proj.Currency = currency
        proj.ProjectManagers = managers
        proj.ProjectStakeHolders = stakeholders
        proj.Description = description
        proj.Log = log
        db.session.commit()

class Tasks(db.Model):
    TaskID = db.Column(db.Integer, primary_key = True)
    TaskCode = db.Column(db.String(20), nullable = False, unique = True)
    project_code = db.Column(db.String(10), db.ForeignKey('project.ProjectCode'),nullable = False)
    Priority = db.Column(db.Integer)
    TaskDescription = db.Column(db.String(1000), nullable = False)
    ExpectedStartDate = db.Column(db.Date)
    ExpectedEndDate = db.Column(db.Date)
    ActualStartDate = db.Column(db.Date)
    ActualEndDate = db.Column(db.Date)
    TaskLocation = db.Column(db.String)
    AssignedTo = db.Column(db.ARRAY(db.String(50)))
    DependsOn = db.Column(db.ARRAY(db.String))
    Dependabilities = db.Column(db.ARRAY(db.String))
    TaskStatus = db.Column(db.String(20))
    Comments = db.Column(db.Text)
    
    def __init__(self, taskcode, projectcode, priority, desc, exstdate, exenddate, actstdate, actenddate, location, assigned, depon, dep, status, comments):
        self.TaskCode = taskcode
        self.project_code = projectcode
        self.Priority = priority
        self.TaskDescription = desc
        self.ExpectedStartDate = exstdate
        self.ExpectedEndDate = exenddate
        self.ActualStartDate = actstdate
        self.ActualEndDate = actenddate
        self.TaskLocation = location
        self.AssignedTo = assigned
        self.DependsOn = depon
        self.Dependabilities = dep
        self.TaskStatus = status
        self.Comments = comments
        db.session.add(self)
        db.session.commit()

    def GetAllProjectTasks(procode):
        qrys = Tasks.query.filter_by(project_code = procode).order_by(Tasks.Priority).all()
        return qrys 

    def GetTaskByCode(procode, taskcode):
        qrys = Tasks.query.filter_by(project_code = procode, TaskCode = taskcode).first()
        return qrys 

    def UpdateTask(procode, taskcode, priority, desc, exstdate, exenddate, actstdate, actenddate, location, assigned, depon, dep, status, comments):
        qry = Tasks.query.filter_by(project_code = procode, TaskCode = taskcode).first()
        qry.TaskDescription = desc
        qry.ExpectedStartDate = exstdate
        qry.ExpectedEndDate = exenddate
        qry.ActualStartDate = actstdate
        qry.ActualEndDate = actenddate
        qry.TaskLocation = location
        qry.AssignedTo = assigned
        qry.DependsOn = depon
        qry.Dependabilities = dep
        qry.TaskStatus = status
        qry.Comments = comments
        db.session.commit()

    

