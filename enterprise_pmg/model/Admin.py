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
        pswd, hashpass =Users.createpassword(self.UserName)
        self.Password = hashpass
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
        qrys = Users.query.order_by(Users.UserId).paginate()
        return qrys

    def GetUserByID(uid):
        qry = Users.query.filter_by(UserId = uid).first()
        return qry

    def GetProfilePic(uname):
        qry = Users.query.filter_by(UserName = uname).first()
        propic = qry.ProfilePic
        return propic
        

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
        return pswd, hashpass

    def SELECT_ALL():
        return Users.query.paginate()

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

    def CHANGE_PASSWORD_BY_USERNAME(username, oldpassword, newpassword):
        m = hashlib.sha256()
        n = hashlib.sha256()
        n.update(oldpassword.encode('utf8'))
        oldhash = n.hexdigest()
        m.update(newpassword.encode('utf8'))
        hashpass = m.hexdigest()
        usr = Users.query.filter_by(UserName = username, Password = oldhash).first()
        usr.Password = hashpass
        db.session.commit()

    def CHANGE_FORGOT_PASSWORD(uname, newpassword):
        m = hashlib.sha256()
        m.update(newpassword.encode('utf8'))
        hashpass = m.hexdigest()
        usr = Users.query.filter_by(UserName = uname).first()
        usr.Password = hashpass
        db.session.commit()

    def RESET_PASSWORD(uid):
        usr = Users.GetUserByID(uid)
        username = usr.UserName
        email = usr.Email
        firstname = usr.FirstName
        pswd = username + '@123'
        m = hashlib.sha256()
        m.update(pswd.encode('utf8'))
        hashpass = m.hexdigest()
        usr.Password = hashpass
        db.session.commit()
        return firstname, pswd, email

    def LOGGER(username, password):
        #try:
        if password != 'admin':
            m = hashlib.sha256()
            m.update(password.encode('utf8'))
            pswd = m.hexdigest()
            usr = Users.query.filter_by(UserName = username, Password = pswd).first()
            if usr:
                if usr.UserName == username and usr.Password == pswd and usr.Status == 'Active':
                    return {'username': usr.UserName, 'role': usr.Role, 'ProPic': usr.ProfilePic, 'Logged': True}
            else:
                return{'Logged': False}
        else:
            usr = Users.query.filter_by(UserName = username, Password = password).first()
            if usr:
                if usr.UserName == username and usr.Password == password and usr.Status == 'Active':
                    return {'username': usr.UserName, 'role': usr.Role, 'ProPic': usr.ProfilePic,'Logged': True}
            else:
                return{'Logged': False}
        #except:
        #    return {'Logged': False}

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
    Logo =  db.Column(db.String(50), nullable = True)

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
        qry =  CompanyProfile.query.filter_by(CompanyID = cid).first()
        return qry
    
    def UpdateCompanyProfile(name, address, phone1, phone2, email, pobox, reg, desc, logo):
        cmp = CompanyProfile.query.first()
        cmp.CompanyName = name
        cmp.Address = address
        cmp.Phone_1 = phone1
        cmp.Phone_2 = phone2
        cmp.Email = email
        cmp.POBox = pobox
        cmp.Registration = reg
        cmp.Description = desc
        cmp.Logo = logo
        db.session.commit()
