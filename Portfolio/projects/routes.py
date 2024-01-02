from Portfolio import db
import flask 
from Portfolio.projects.forms import ProjectForm
from flask import render_template, url_for,flash,redirect,request
from Portfolio.models import Project
from flask_login import login_user,current_user,login_required
from flask import Blueprint 

projects_blueprint = Blueprint('projects_blueprint',__name__)

@projects_blueprint.route("/projects",methods=['GET'])
@login_required
def projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html',projects=projects)

@projects_blueprint.route("/projects/<int:project_id>",methods=['GET','POST'])
@login_required
def curr_project(project_id):
    # projects = Project.query.filter_by(user_id=current_user.id).all()
    curr_project = Project.query.get_or_404(project_id)
    return render_template('curr_projects.html',curr_project=curr_project)


@projects_blueprint.route("/projects/<int:project_id>/update",methods=['GET','POST'])
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
        return redirect(url_for('projects_blueprint.projects'))
    elif request.method == "GET":
        form.project_title.data = curr_project.project_title
        form.project_overview.data = curr_project.project_overview
        form.project_url.data = curr_project.project_url
    return render_template('projects.add_project.html',curr_project=curr_project,form=form)

@projects_blueprint.route("/projects/<int:project_id>/delete",methods=['POST'])
@login_required
def delete_project(project_id):
    curr_project = Project.query.get_or_404(project_id)
    db.session.delete(curr_project)
    db.session.commit()
    flash("Your project has been deleted",'success')
    return redirect(url_for('projects_blueprint.projects'))

@projects_blueprint.route("/projects/add_projects",methods=['GET','POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(project_title=form.project_title.data, project_overview=form.project_overview.data,
                           project_url=form.project_url.data,user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Your Project has been added !!','success')
        return redirect(url_for('projects_blueprint.projects'))
    return render_template('add_project.html',form=form)