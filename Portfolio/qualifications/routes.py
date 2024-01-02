from Portfolio import app,db,bcrypt 
import flask 
from Portfolio.forms import LoginForm,RegistrationForm ,EditProfile,ProjectForm,create_skill_form,QualificationsForm,searchForm
from flask import render_template, url_for,flash,redirect,request,session,get_flashed_messages
from Portfolio.models import User,Project,Skills,Qualifications
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os 
from PIL import Image
from urllib.parse import urlparse, urljoin

@app.route("/qualifications", methods=['GET', 'POST'])
@login_required
def qualifications():
    user_qualifications = Qualifications.query.filter_by(user_id=current_user.id).all()
    return render_template('qualifications.html', user_qualifications=user_qualifications)

@app.route("/qualifications/add_qualification", methods=['GET', 'POST'])
@login_required
def add_qualification():
    form = QualificationsForm()
    if form.validate_on_submit():
        Course = Qualifications(course=form.course.data,user_id = current_user.id)
        db.session.add(Course)
        db.session.commit()
        flash("Your Quallification has been added!!",'success')
        return redirect(url_for('qualifications'))
   
    return render_template('add_qualification.html', form=form)


@app.route("/qualifications/<int:qualification_id>",methods=['GET','POST'])
@login_required
def curr_qualification(qualification_id):
    # projects = Project.query.filter_by(user_id=current_user.id).all()
    curr_qualification = Qualifications.query.get_or_404(qualification_id)
    return render_template('curr_qualification.html',curr_qualification=curr_qualification)

@app.route("/qualifications/<int:qualification_id>/update",methods=['GET','POST'])
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
        return redirect(url_for('qualifications'))
    elif request.method == "GET":
        form.course.data = curr_qualification.course
    return render_template('add_qualification.html',curr_qualification=curr_qualification,form=form)

@app.route("/qualifications/<int:qualification_id>/delete",methods=['POST'])
@login_required
def delete_qualification(qualification_id):
    curr_qualification = Qualifications.query.get_or_404(qualification_id)
    db.session.delete(curr_qualification)
    db.session.commit()
    flash("Your qualifications has been deleted",'success')
    return redirect(url_for('qualifications'))
