from app import db
import hashlib

class Users(db.Model):
    UserId = db.Column(db.Integer, primary_key = True)
    FirstName = db.Column(db.String(50), nullable = False)
    LastName = db.Column(db.String(50), nullable = False)
    UserName db.Column(db.String(50), nullable = False)
    Password = db.Column(db.String(500), nullable = False)
    Position = db.Column(db.String(50), nullable = True)
    Department = db.Column(db.String(50), nullable = True)
    Email = db.Column(db.String(100), nullable = True)
    Phone = db.Column(db.String(50), nullable = True)
    Role = db.Column(db.ARRAY(db.String(50)), nullable = False)
    Status = db.Column(db.String(10), nullable = False)
    ProfilePic = db.Column(db.String(50), nullable = True)
    db.UniqueConstraint(UserName)

    def __init__(self, firstname, lastname, position, department, email, phone, role, status, profilepic):
        self.FirstName = firstname
        self.LastName = lastname
        self.UserName = createusername(firstname, lastname)
        self.Password = createpassword(self.UserName)
        self.Position = position
        self.Department = department
        self.Email = email
        self.Phone = phone
        self.Role = role
        self.status = Status
        self.ProfilePic = profilepic  

    def createusername(self, firstname, lastname):
        user = firstname[0].lower() + lastname.lower()
        i = 1
        userexists = Users.query.all()
        for name in userexists.UserName:
            while user == userexists.UserName:
                newname = user + str(i)
                i += 1
        return newname

    def createpassword(self, username):
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
            if usr.UserName == username and usr.Password == pswd and usr.Status == 'Active':
                return {'username': usr.UserName, 'role': usr.Role, 'Logged': True}
            else:
                return{'Logged': False}

