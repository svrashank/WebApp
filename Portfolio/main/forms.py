from flask_wtf import FlaskForm 
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,EmailField,TextAreaField,DateField
from wtforms.validators import DataRequired,Length, ValidationError
from Portfolio.models import User 
from flask_login import current_user


class EditProfile(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = EmailField('Email',validators=[DataRequired()])
    picture = FileField("Update Profile Picture",validators=[FileAllowed(['jpg','png'])])
    profile_overview = TextAreaField("Profile Overview",validators=[Length(min=0,max=180)],render_kw={'rows': 3})
    skill = StringField("Skill")
    experience = StringField("Experience")
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
                # <a href="{{url_for('users_blueprint.sign_in')}}"> Logging in</a>
                raise ValidationError ('Already have an account?Try logging in')

class searchForm(FlaskForm):
    input = StringField('input')
    search = SubmitField('Search')