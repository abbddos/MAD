from flask_restful import Api, Resource
from datetime import datetime, date
from enterprise_pmg.model import Projects, Admin

class GetAllProjects(Resource):
    def get(self):
        qrys = Projects.Project.GET_ALL_PROJECTS()
        data1 = []
        for qry in qrys:
            data = dict()
            data['ProjectID'] = qry.ProjectID
            data['ProjectCode'] = qry.ProjectCode
            data['StartDate'] = str(qry.StartDate)
            data['EndDate'] = str(qry.EndDate)
            data['Location'] = qry.Location
            data['FundingSource'] = qry.FundingSource
            data['TotalBudget'] = qry.TotalBudget
            data['Currency'] = qry.Currency
            data['ProjectManagers'] = qry.ProjectManagers
            data['StakeHolders'] = qry.ProjectStakeHolders
            data['Description'] = qry.Description
            data['Log'] = qry.Log
            data1.append(data)
        return {'Projects': data1}

class GetProjectByID(Resource):
    def get(self,pid):
        qry = Projects.Project.GetProjectByID(pid)
        data = dict()
        data['ProjectID'] = qry.ProjectID
        data['ProjectCode'] = qry.ProjectCode
        data['StartDate'] = str(qry.StartDate)
        data['EndDate'] = str(qry.EndDate)
        data['Location'] = qry.Location
        data['FundingSource'] = qry.FundingSource
        data['TotalBudget'] = qry.TotalBudget
        data['Currency'] = qry.Currency
        data['ProjectManagers'] = qry.ProjectManagers
        data['StakeHolders'] = qry.ProjectStakeHolders
        data['Description'] = qry.Description
        data['Log'] = qry.Log
        return data

class GetProjectByCode(Resource):
    def get(self,code):
        qry = Projects.Project.GetProjectByCode(code)
        data = dict()
        data['ProjectID'] = qry.ProjectID
        data['ProjectCode'] = qry.ProjectCode
        data['StartDate'] = str(qry.StartDate)
        data['EndDate'] = str(qry.EndDate)
        data['Location'] = qry.Location
        data['FundingSource'] = qry.FundingSource
        data['TotalBudget'] = qry.TotalBudget
        data['Currency'] = qry.Currency
        data['ProjectManagers'] = qry.ProjectManagers
        data['StakeHolders'] = qry.ProjectStakeHolders
        data['Description'] = qry.Description
        data['Log'] = qry.Log
        return data

class GetAllProjectTasks(Resource):
    def get(self, procode):
        qrys = Projects.Tasks.GetAllProjectTasks(procode)
        data1 = []
        for qry in qrys:
            data = dict()
            data['TaskID'] = qry.TaskID
            data['TaskCode'] = qry.TaskCode
            data['ProjectCode'] = qry.project_code
            data['Priority'] = qry.Priority
            data['TaskDescription'] = qry.TaskDescription
            data['ExpectedStartDate'] = str(qry.ExpectedStartDate)
            data['ExpectedEndDate'] = str(qry.ExpectedEndDate)
            data['ActualStartDate'] = str(qry.ActualStartDate)
            data['ActualEndDate'] = str(qry.ActualEndDate)
            data['Location'] = qry.Location
            data['AssignedTo'] = qry.AssignedTo
            data['Deliverables'] = qry.Deliverables
            data['DependsOn'] = qry.DependsOn
            data['Dependability'] = qry.Dependabilities
            data['TaskStatus'] = qry.TaskStatus
            data['Comments'] = qry.Comments
            data1.append(data)
        return data1

class GetTaskByCode(Resource):
    def get(self, procode, taskcode):
        qry = Projects.Tasks.GetTaskByCode(procode, taskcode)
        data = dict()
        data['TaskID'] = qry.TaskID
        data['TaskCode'] = qry.TaskCode
        data['ProjectCode'] = qry.project_code
        data['Priority'] = qry.Priority
        data['TaskDescription'] = qry.TaskDescription
        data['ExpectedStartDate'] = str(qry.ExpectedStartDate)
        data['ExpectedEndDate'] = str(qry.ExpectedEndDate)
        data['ActualStartDate'] = str(qry.ActualStartDate)
        data['ActualEndDate'] = str(qry.ActualEndDate)
        data['Location'] = qry.Location
        data['AssignedTo'] = qry.AssignedTo
        data['Deliverables'] = qry.Deliverables
        data['DependsOn'] = qry.DependsOn
        data['Dependability'] = qry.Dependabilities
        data['TaskStatus'] = qry.TaskStatus
        data['Comments'] = qry.Comments
        return data
    
           


