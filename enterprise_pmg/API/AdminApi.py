
from flask_restful import Api, Resource
#from enterprise_pmg import api
from enterprise_pmg.model import Admin

class GetAllUsers(Resource):
    def get(self):
        qrys = Admin.Users.GetAllUsers()
        data1 = []
        for qry in qrys.items:
            data = {}
            data['UserId'] = qry.UserId
            data['FirstName'] = qry.FirstName
            data['LastName'] = qry.LastName
            data['UserName'] = qry.UserName
            data['Position'] = qry.Position
            data['Department'] = qry.Department
            data['Email'] = qry.Email
            data['Phone'] = qry.Phone
            data['Role'] = qry.Role
            data['Status'] = qry.Status
            data['ProfilePic'] = qry.ProfilePic
            data1.append(data)
        return {'info': data1}
    
class GetUserByID(Resource):
    def get(self, uid):
        data = dict()
        qry = Admin.Users.GetUserByID(uid)
        data['UserId'] = qry.UserId
        data['FirstName'] = qry.FirstName
        data['LastName'] = qry.LastName
        data['UserName'] = qry.UserName
        data['Position'] = qry.Position
        data['Department'] = qry.Department
        data['Email'] = qry.Email
        data['Phone'] = qry.Phone
        data['Role'] = qry.Role
        data['Status'] = qry.Status
        data['ProfilePic'] = qry.ProfilePic
        return data

class GetCompanyByID(Resource):
    def get(self, cid):
        qry = Admin.CompanyProfile.GetCompanyByID(cid)
        data = dict()
        data['CompanyID'] = qry.CompanyID
        data['CompanyName'] = qry.CompanyName
        data['Address'] = qry.Address
        data['Phone_1'] = qry.Phone_1
        data['Phone_2'] = qry.Phone_2
        data['Email'] = qry.Email
        data['POBox'] = qry.POBox
        data['Registration'] = qry.Registration
        data['Description'] = qry.Description
        data['Logo'] = qry.Logo
        return data