from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField

class QualificationsForm(FlaskForm):
    update = SubmitField("Update")
    course = StringField('Course')
