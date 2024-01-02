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


@app.route("/projects",methods=['GET'])
@login_required
def projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html',projects=projects)

@app.route("/projects/<int:project_id>",methods=['GET','POST'])
@login_required
def curr_project(project_id):
    # projects = Project.query.filter_by(user_id=current_user.id).all()
    curr_project = Project.query.get_or_404(project_id)
    return render_template('curr_projects.html',curr_project=curr_project)


@app.route("/projects/<int:project_id>/update",methods=['GET','POST'])
@login_required
def update_project(project_id):
    form = ProjectForm()
    curr_project = Project.query.get_or_404(project_id)
    if form.validate_on_submit():
        curr_project.project_title = form.project_title.data
        curr_project.project_overview = form.project_overview.data
        curr_project.project_url = form.project_url.data
        db.session.commit()
        flash(f"Your project {curr_project.project_title} has been updated",'success')
        return redirect(url_for('projects'))
    elif request.method == "GET":
        form.project_title.data = curr_project.project_title
        form.project_overview.data = curr_project.project_overview
        form.project_url.data = curr_project.project_url
    return render_template('add_project.html',curr_project=curr_project,form=form)

@app.route("/projects/<int:project_id>/delete",methods=['POST'])
@login_required
def delete_project(project_id):
    curr_project = Project.query.get_or_404(project_id)
    db.session.delete(curr_project)
    db.session.commit()
    flash("Your project has been deleted",'success')
    return redirect(url_for('projects'))

@app.route("/projects/add_projects",methods=['GET','POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(project_title=form.project_title.data, project_overview=form.project_overview.data,
                           project_url=form.project_url.data,user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Your Project has been added !!','success')
        return redirect(url_for('projects'))
    return render_template('add_project.html',form=form)