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
    # There should be foreign keys to be added and linked to tasks, budgets and WBSs

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