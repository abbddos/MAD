from enterprise_pmg import db
import hashlib

class Users(db.Model):
    UserId = db.Column(db.Integer, primary_key = True)
    FirstName = db.Column(db.String(50), nullable = False)
    LastName = db.Column(db.String(50), nullable = False)
    UserName = db.Column(db.String(50), nullable = False, unique = True)
    Password = db.Column(db.String(500), nullable = False)
    Position = db.Column(db.String(50), nullable = True)
    Department = db.Column(db.String(50), nullable = True)
    Email = db.Column(db.String(100), nullable = True)
    Phone = db.Column(db.String(50), nullable = True)
    Role = db.Column(db.ARRAY(db.String(50)), nullable = False)
    Status = db.Column(db.String(10), nullable = False)
    ProfilePic = db.Column(db.String(50), nullable = True)
    

    def __init__(self, firstname, lastname, position, department, email, phone, role, status, profilepic):
        self.FirstName = firstname
        self.LastName = lastname
        self.UserName = Users.createusername(firstname, lastname)
        self.Password = Users.createpassword(self.UserName)
        self.Position = position
        self.Department = department
        self.Email = email
        self.Phone = phone
        self.Role = role
        self.Status = status
        self.ProfilePic = profilepic  
        db.session.add(self)
        db.session.commit()

    def GetAllUsers():
        data1 = []
        qrys = Users.query.all()
        for qry in qrys:
            data = dict()
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
        return data1

    def GetUserByID(uid):
        qry = Users.query.filter_by(UserId = uid).first()
        data = dict()
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
        

    def createusername(firstname, lastname):
        user = firstname[0].lower() + lastname.lower()
        newname = user
        i = 1
        userexists = Users.query.all()
        for name in userexists:
            while newname == name.UserName:
                newname = user + str(i)
                i += 1
        return newname

    def createpassword(username):
        pswd = username + '@123'
        m = hashlib.sha256()
        m.update(pswd.encode('utf8'))
        hashpass = m.hexdigest()
        return hashpass

    def SELECT_ALL():
        return Users.query.all()

    def SELECT_ONE_USER(username):
        return Users.query.filter_by(UserName = username).first()

    def UPDATE_ONE_USER(uid, firstname, lastname, position, department, email, phone, role, status, profilepic):
        updateduser = Users.query.filter_by(UserId = uid).first()
        updateduser.FirstName = firstname
        updateduser.LastName = lastname
        updateduser.Position = position
        updateduser.Department = department
        updateduser.Email = email
        updateduser.Phone = phone
        updateduser.Role = role
        updateduser.Status = status
        updateduser.ProfilePic = profilepic
        db.session.commit()

    def CHANGE_PASSWORD_BY_USERNAME(username, newpassword):
        m = hashlib.sha256()
        m.update(newpassword.encode('utf8'))
        hashpass = m.hexdigest()
        usr = Users.query.filter_by(UserName = username).first()
        usr.Password = hashpass
        db.session.commit()

    def CHANGE_PASSWORD_BY_EMAIL(email, newpassword):
        m = hashlib.sha256()
        m.update(newpassword.encode('utf8'))
        hashpass = m.hexdigest()
        usr = Users.query.filter_by(Email = email).first()
        usr.Password = hashpass
        db.session.commit()

    def LOGGER(username, password):
        if password != 'admin':
            m = hashlib.sha256()
            m.update(password.encode('utf8'))
            pswd = m.hexdigest()
            usr = Users.query.filter_by(UserName = username, Password = pswd).first()
            if usr.UserName == username and usr.Password == pswd and usr.Status == 'Active':
                return {'username': usr.UserName, 'role': usr.Role, 'Logged': True}
            else:
                return{'Logged': False}
        else:
            usr = Users.query.filter_by(UserName = username, Password = password).first()
            if usr.UserName == username and usr.Password == password and usr.Status == 'Active':
                return {'username': usr.UserName, 'role': usr.Role, 'Logged': True}
            else:
                return{'Logged': False}

class CompanyProfile(db.Model):
    CompanyID = db.Column(db.Integer, primary_key = True)
    CompanyName = db.Column(db.String(1000))
    Address = db.Column(db.String(50))
    Phone_1 =  db.Column(db.String(20))
    Phone_2 = db.Column(db.String(20))
    Email = db.Column(db.String(50))
    POBox = db.Column(db.String(10))
    Registration = db.Column(db.String(50))
    Description = db.Column(db.Text) 

    def __init__(self, name, address, phone1, phone2, email, pobox, reg, desc):
        self.CompanyName = name
        self.Address = address
        self.Phone_1 = phone1
        self.Phone_2 = phone2
        self.Email = email
        self.POBox = pobox
        self.Registration = reg
        self.Description = desc

    def GetCompanyByID(cid):
        data = dict()
        qry =  CompanyProfile.query.filter_by(CompanyID = cid).first()
        data['CompanyID'] = qry.CompanyID
        data['CompanyName'] = qry.CompanyName
        data['Address'] = qry.Address
        data['Phone_1'] = qry.Phone_1
        data['Phone_2'] = qry.Phone_2
        data['Email'] = qry.Email
        data['POBox'] = qry.POBox
        data['Registration'] = qry.Registration
        data['Description'] = qry.Description
        return data
    
    def UpdateCompanyProfile(name, address, phone1, phone2, email, pobox, reg, desc):
        cmp = CompanyProfile.query.first()
        cmp.CompanyName = name
        cmp.Address = address
        cmp.Phone_1 = phone1
        cmp.Phone_2 = phone2
        cmp.Email = email
        cmp.POBox = pobox
        cmp.Registration = reg
        cmp.Description = desc
        db.session.commit()
