from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField,TextAreaField

class ProjectForm(FlaskForm):
    projects = StringField("Projects")
    project_title = StringField("Title")
    project_overview =TextAreaField("Overview",render_kw={'row':3})
    project_url =StringField("Link")
    add = SubmitField("Add")
    done = SubmitField("Done")
    # remove = SubmitField('Remove')