from Portfolio import db
import flask
from flask import Blueprint 
from Portfolio.main.forms import EditProfile,searchForm
from flask import render_template, url_for,flash,redirect,request
from Portfolio.models import User,Project,Skills,Qualifications
from flask_login import login_user,current_user,logout_user,login_required
from Portfolio.main.utils import save_picture,save_resume

main = Blueprint('main',__name__)

@main.route("/home",methods=['GET','POST'])
def home():
    form = searchForm()
    page = request.args.get('page',1,type=int)
    users = User.query.paginate(per_page=3,page=page)
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.input.data.strip()).first()
        if user:
            return redirect(url_for('main.home_search',username=form.input.data.strip()))
        else:
            return redirect(url_for('main.user_not_found'))
    return render_template("home.html",users=users,form=form )

@main.route("/home/<username>",methods=['GET','POST'])
def home_search(username):
    user = User.query.filter_by(username=username).first()
    return render_template("home_search.html",user=user)

@main.route("/home/user_not_found")
def user_not_found():
    return render_template('user_not_found.html')

@main.route("/user/<username>")
def user_profile(username):
    # page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    projects = Project.query.filter_by(user_id = user.id)
    skills = Skills.query.filter_by(user_id = user.id)
    qualifications = Qualifications.query.filter_by(user_id = user.id)
    return render_template("user_profile.html",user=user,projects=projects,skills=skills,qualifications=qualifications)

# @main.route("/yourprofile",methods=['GET','POST'])
# @login_required
# def yourprofile():
#     image_file = url_for('static',filename='/profile_pics/'+current_user.image_file)
#     return render_template('yourprofile.html',title='Your Profile',image_file=image_file)



@main.route("/editprofile",methods=['GET','POST'])
@login_required
def editprofile():
    form = EditProfile()
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if form.dob.data:
            if form.dob.data != current_user.DOB:
                current_user.DOB = form.dob.data
        if form.resume.data :
            resume_file = save_resume(form.resume.data)
            current_user.resume = resume_file
        if form.profile_overview.data :
            if form.profile_overview.data != current_user.profile_overview:
                current_user.profile_overview =form.profile_overview.data
        if form.experience.data :
            current_user.experience = form.experience.data 
        current_user.email = form.email.data 
        current_user.username = form.username.data 
        db.session.commit()
        flash("Your Profile has been updated!!",'success')
        return redirect(url_for('main.editprofile'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email 
        form.dob.data = current_user.DOB
        form.profile_overview.data = current_user.profile_overview
        form.experience.data = current_user.experience
    return render_template('editprofile.html',image_file=image_file,title='Edit profile',form = form)


@main.route("/sign_out")
def sign_out():
    logout_user()
    return redirect(url_for('main.home'))

