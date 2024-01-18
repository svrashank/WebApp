from Portfolio import db
import flask 
from Portfolio.qualifications.forms import QualificationsForm
from flask import render_template, url_for,flash,redirect,request
from Portfolio.models import Qualifications
from flask_login import current_user,login_required
from flask import Blueprint 

qualifications_blueprint = Blueprint('qualifications_blueprint',__name__)

@qualifications_blueprint.route("/qualifications", methods=['GET', 'POST'])
@login_required
def qualifications():
    user_qualifications = Qualifications.query.filter_by(user_id=current_user.id).all()
    return render_template('qualifications.html', user_qualifications=user_qualifications)

@qualifications_blueprint.route("/qualifications/add_qualification", methods=['GET', 'POST'])
@login_required
def add_qualification():
    form = QualificationsForm()
    if form.validate_on_submit():
        Course = Qualifications(course=form.course.data,user_id = current_user.id)
        db.session.add(Course)
        db.session.commit()
        flash("Your Quallification has been added!!",'success')
        return redirect(url_for('qualifications_blueprint.qualifications'))
   
    return render_template('add_qualification.html', form=form)


@qualifications_blueprint.route("/qualifications/<int:qualification_id>",methods=['GET','POST'])
@login_required
def curr_qualification(qualification_id):
    curr_qualification = Qualifications.query.get_or_404(qualification_id)
    return render_template('curr_qualification.html',curr_qualification=curr_qualification)

@qualifications_blueprint.route("/qualifications/<int:qualification_id>/update",methods=['GET','POST'])
@login_required
def update_qualification(qualification_id):
    form = QualificationsForm()
    curr_qualification = Qualifications.query.get_or_404(qualification_id)
    if form.validate_on_submit():
        print(f"Form data before update: {form.course.data}")
        print(f"Current qualification course before update: {curr_qualification.course}")
        curr_qualification.course = form.course.data

        db.session.commit()
        flash(f"Your qualifications {curr_qualification.course} has been updated",'success')
        return redirect(url_for('qualifications_blueprint.qualifications'))
    elif request.method == "GET":
        form.course.data = curr_qualification.course
    return render_template('add_qualification.html',curr_qualification=curr_qualification,form=form)

@qualifications_blueprint.route("/qualifications/<int:qualification_id>/delete",methods=['POST'])
@login_required
def delete_qualification(qualification_id):
    curr_qualification = Qualifications.query.get_or_404(qualification_id)
    db.session.delete(curr_qualification)
    db.session.commit()
    flash("Your qualifications has been deleted",'success')
    return redirect(url_for('qualifications_blueprint.qualifications'))
