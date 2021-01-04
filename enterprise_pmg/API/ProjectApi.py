from flask_restful import Api, Resource
from datetime import datetime, date
from enterprise_pmg.model import Project, Admin

class GetAllProjects(Resource):
    def get(self):
        qrys = Project.Project.GetAllProjects()
        data1 = []
        for qry in qrys.items:
            data = dict()
            data['ProjectID'] = qry.ProjectID
            data['ProjectCode'] = qry.ProjectCode
            data['StartDate'] = qry.StartDate
            data['EndDate'] = qry.EndDate
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
        qry = Project.Project.GetProjectByID(pid)
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
        qry = Project.Project.GetProjectByCode(code)
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

