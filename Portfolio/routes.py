from Portfolio import app,db,bcrypt 
import flask 
from Portfolio.forms import LoginForm,RegistrationForm ,EditProfile,ProjectForm,create_skill_form,QualificationsForm
from flask import render_template, url_for,flash,redirect,request,session,get_flashed_messages
from Portfolio.models import User,Project,Skills,Qualifications
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os 
from PIL import Image



from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route("/",methods=['GET','POST'])
def sign_in():
    if current_user.is_authenticated:
        flash(f"logged in as {current_user.username}")
        return redirect(url_for("home"))
    form  = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f"Login successful for {form.email.data}",'success')
            next = request.args.get('next')
            if next and not is_safe_url(next):
                return flask.abort(400)
            return redirect(next or url_for('home')) 
        else:
            flash("Wrong email or password,please try again",'error')
    return render_template("signin.html",title = "Login",form = form)




@app.route("/signup",methods=['GET','POST'])
def sign_up():  
    if current_user.is_authenticated:
        flash(f"logged in as{current_user.username}")
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Hash Password and store all information in the database 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data,email = form.email.data,password = hashed_password)
        # app.app_context().push()
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}",'success')
        return redirect(url_for('home'))
    if request.method == "POST":
        # for field,error in form.errors.items():
        #     flash(error [0], f'danger_{field}')
        # else:
        #     flash("Account not created. Please check your inputs.", 'danger')
        return render_template("sign_up.html",title ="Sign Up",form = form)

    return render_template("sign_up.html",title ="Sign Up",form = form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path,"static/profile_pics",picture_filename)
    form_picture.save(picture_path)
    # output_size = (125,125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)
    return picture_filename

def save_resume(form_resume_file):
    random_hex = secrets.token_hex(8)
    _,file_ext = os.path.splitext(form_resume_file.filename)
    resume_filename = random_hex + file_ext
    file_path = os.path.join(app.root_path,"static/resume",resume_filename)
    form_resume_file.save(file_path)
    return resume_filename

@app.route('/show_signup')
def show_sign_up():
    return render_template("sign_up.html", title="Sign Up", form=RegistrationForm())

 
@app.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    users = User.query.paginate(per_page=3,page=page)
    return render_template("home.html",users=users)

@app.route("/user/<username>")
def user_profile(username):
    # page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    projects = Project.query.filter_by(user_id = user.id)
    skills = Skills.query.filter_by(user_id = user.id)
    qualifications = Qualifications.query.filter_by(user_id = user.id)
    return render_template("user_profile.html",user=user,projects=projects,skills=skills,qualifications=qualifications)

@app.route("/yourprofile",methods=['GET','POST'])
@login_required
def yourprofile():
    image_file = url_for('static',filename='/profile_pics/'+current_user.image_file)
    return render_template('yourprofile.html',title='Your Profile',image_file=image_file)



@app.route("/editprofile",methods=['GET','POST'])
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
        current_user.email = form.email.data 
        current_user.username = form.username.data 
        db.session.commit()
        flash("Your Profile has been updated!!",'success')
        return redirect(url_for('editprofile'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email 
        form.dob.data = current_user.DOB
        form.profile_overview.data = current_user.profile_overview
        form.experience.data = current_user.experience
    return render_template('editprofile.html',image_file=image_file,title='Edit profile',form = form)



def delete_user(user_id):
    # Get the user by ID
    user = User.query.get(user_id)

    if user:
        try:
            # Delete associated data (profile, project, skills, qualifications)
            print(f"Deleting associated data for user {user_id}")
            Project.query.filter_by(user_id=user.id).delete()
            Skills.query.filter_by(user_id=user.id).delete()
            Qualifications.query.filter_by(user_id=user.id).delete()

            # Delete the user
            print(f"Deleting user {user_id}")   
            db.session.delete(user)
            db.session.commit()

            print(f"User {user_id} deleted successfully")
            return True
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print(f"Error deleting user {user_id}: {e}")
            db.session.rollback()
            return False
    else:
        print(f"User {user_id} not found")
        return False


@app.route("/editprofile/delete",methods = ["GET","POST"])
@login_required
def delete_account():
    user_id = current_user.id
    delete_user(user_id)
    return redirect(url_for('sign_up'))

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

@app.route("/other interests")
@login_required
def other_interests():
    return render_template('other_interests.html')

@app.route("/sign_out")
def sign_out():
    logout_user()
    return redirect(url_for('home'))

@app.route("/skills/add_skill",methods=['GET','POST'])
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
        return redirect(url_for('skills'))

    if request.method == 'GET':
        existing_skills = Skills.query.filter_by(user_id=current_user.id).all()

        for i, skill in enumerate(existing_skills, start=1):
            if i <= 7:
                form[f'skill_{i}'].data = skill.skill_name
                form[f'skill_value_{i}'].data = skill.skill_value


    return render_template('add_skill.html',form = form)

@app.route("/skills",methods=['GET','POST'])
def skills():
    user_skills = Skills.query.filter_by(user_id=current_user.id).all() 
    return render_template('skills.html',user_skills=user_skills)






