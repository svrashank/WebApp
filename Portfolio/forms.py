from flask_wtf import FlaskForm 
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, BooleanField,SubmitField,EmailField,validators,SelectField,TextAreaField,DateField, IntegerField
from wtforms.validators import DataRequired,Length, EqualTo, ValidationError
from Portfolio import app,db
from Portfolio.models import User 
from flask import redirect
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = EmailField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_username(self,username):
        curr_user = User.query.filter_by(username=username.data).first()
        if curr_user:
            raise ValidationError('Username already exists, please try a different one')
    def validate_email(self,email):
        curr_user = User.query.filter_by(email=email.data).first()
        if curr_user:
            # <a href="{{url_for('sign_in')}}"> Logging in</a>
            raise ValidationError ('Already have an account?Try logging in')
            

class LoginForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login') 
    
class EditProfile(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = EmailField('Email',validators=[DataRequired()])
    picture = FileField("Update Profile Picture",validators=[FileAllowed(['jpg','png'])])
    profile_overview = TextAreaField("Profile Overview",validators=[DataRequired(),Length(min=10,max=180)],render_kw={'rows': 3})
    skill = StringField("Skill")
    skill_value = IntegerField("Skill Range")
    projects = StringField("Projects")
    dob = DateField("Date of Birth")
    resume = FileField("Upload Resume",validators=[FileAllowed(['pdf'])])
    qualification = TextAreaField("Qualifications")
    update = SubmitField('Update')

    def validate_username(self,username):
        if current_user.username != username.data:
            curr_user = User.query.filter_by(username=username.data).first()
            if curr_user:
                raise ValidationError('Username already exists, please try a different one')
            
    def validate_email(self,email):
        if current_user.email != email.data:
            curr_user = User.query.filter_by(email=email.data).first()
            if curr_user:
                # <a href="{{url_for('sign_in')}}"> Logging in</a>
                raise ValidationError ('Already have an account?Try logging in')
        
class ProjectForm(FlaskForm):
    projects = StringField("Projects")
    project_title = StringField("Title")
    project_overview =TextAreaField("Overview",render_kw={'row':3})
    project_url =StringField("Link")
    add = SubmitField("Add")
    done = SubmitField("Done")
    # remove = SubmitField('Remove')

class SkillForm(FlaskForm):
    skills =[]
    skill_values = []
    for i in range(1,8):
        skill = StringField(f"Skill {i}")
        skill_value = IntegerField(f"Skill {i} Range")
        skills.append(skill)
        skill_values.append(skill_value)
    add = SubmitField("Add")
    