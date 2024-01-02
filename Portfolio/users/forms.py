from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField,SubmitField,EmailField
from wtforms.validators import DataRequired,Length, EqualTo, ValidationError
from Portfolio.models import User 


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
            # <a href="{{url_for('users_blueprint.sign_in')}}"> Logging in</a>
            raise ValidationError ('Already have an account?Try logging in')
            

class LoginForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login') 
    