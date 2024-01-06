from Portfolio import db 
import flask 
from Portfolio.skills.forms import create_skill_form
from flask import render_template, url_for,flash,redirect,request
from Portfolio.models import Skills
from flask_login import current_user
from flask import Blueprint 

skills_blueprint = Blueprint('skills_blueprint',__name__)


@skills_blueprint.route("/skills/add_skill",methods=['GET','POST'])
def add_skill():
    form = create_skill_form()
    skills =[request.form.get(f"skill_{i}") for i in range(1,8)]
    skill_values =[request.form.get(f"skill_value_{i}") for i in range(1,8)]

    if form.validate_on_submit():
    # Fetch existing skills data from the database for the current user
        existing_skills = Skills.query.filter_by(user_id=current_user.id).all()

        # Update the existing skills or create new ones if needed
        for i, (skill_name, skill_value) in enumerate(zip(skills, skill_values), start=1):
            if i <= 7:
                # Check if a skill with the same name already exists
                existing_skill = next((s for s in existing_skills if s.skill_name == skill_name), None)

                if existing_skill:
                    # Update the existing skill
                    existing_skill.skill_value = skill_value
                else:
                    # Create a new skill
                    new_skill = Skills(skill_name=skill_name, skill_value=skill_value, user_id=current_user.id)
                    db.session.add(new_skill)

        db.session.commit()
        flash('Your skills have been updated', 'info')
        return redirect(url_for('skills_blueprint.skills'))

    if request.method == 'GET':
        existing_skills = Skills.query.filter_by(user_id=current_user.id).all()

        for i, skill in enumerate(existing_skills, start=1):
            if i <= 7:
                form[f'skill_{i}'].data = skill.skill_name
                form[f'skill_value_{i}'].data = skill.skill_value


    return render_template('add_skill.html',form = form)

@skills_blueprint.route("/skills",methods=['GET','POST'])
def skills():
    user_skills = Skills.query.filter_by(user_id=current_user.id).all() 
    return render_template('skills.html',user_skills=user_skills)
