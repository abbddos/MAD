
from flask_restful import Api, Resource
#from enterprise_pmg import api
from enterprise_pmg.model import Admin

class GetAllUsers(Resource):
    def get(self):
        return Admin.Users.GetAllUsers()
    
class GetUserByID(Resource):
    def get(self, uid):
        return Admin.Users.GetUserByID(uid)

class GetCompanyByID(Resource):
    def get(self, cid):
        return Admin.CompanyProfile.GetCompanyByID(cid)