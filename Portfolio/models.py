from Portfolio import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(60),nullable=False)
    DOB = db.Column(db.Date)
    resume = db.Column(db.String(20))
    profile_overview = db.Column(db.Text)
    experience = db.Column(db.Text) 
    project = db.relationship('Project',backref='author',lazy=True)
    skill = db.relationship("Skills",backref='author',lazy=True)
    qualification = db.relationship("Qualifications",backref='author',lazy=True)
    def __repr__(self) -> str:
        return f"User('{self.username}'|| '{self.email}'|| '{self.DOB}')"


class Project(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    project_title = db.Column(db.String(100),nullable = False)
    project_overview = db.Column(db.Text,nullable = False)
    project_url = db.Column(db.String(300),nullable = False)

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self) -> str:
        return f"{self.project_title}"
        
class Skills(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    skill_name = db.Column(db.String(50))
    skill_value = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)

    def __repr__(self) -> str:
        return f"{self.skill_name} || {self.skill_value} || {self.user_id}"
    

class Qualifications(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    course = db.Column(db.String(100))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)

    def __repr__(self) -> str:
        return f"{self.course_title} || {self.user_id}"


