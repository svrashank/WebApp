from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import NumberRange


class SkillForm(FlaskForm):
    update = SubmitField("Update")

def create_skill_form():
    class DynamicSkillForm(SkillForm):
        pass

    for i in range(1, 8):
        setattr(DynamicSkillForm, f'skill_{i}', StringField(f"Skill {i}"))
        setattr(DynamicSkillForm, f'skill_value_{i}', IntegerField(f"Skill {i} Range",validators=[NumberRange(min=0,max=100)]))

    return DynamicSkillForm()


