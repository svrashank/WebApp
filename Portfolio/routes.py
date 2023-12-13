from Portfolio import app,db,bcrypt 
import flask 
from Portfolio.forms import LoginForm,RegistrationForm ,EditProfile,ProjectForm,SkillForm
from flask import render_template, url_for,flash,redirect,request,session,get_flashed_messages
from Portfolio.models import User,Profile,Project 
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
            flash("Wrong email or password,please try again")
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
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
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

@app.route("/qualifications")
@login_required
def qualifications():
    return render_template("qualifications.html")
 
@app.route("/home")
def home():
    return render_template("home.html")


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
        current_user.email = form.email.data 
        current_user.username = form.username.data 
        db.session.commit()
        flash("Your Profile has been updated!!",'success')
        return redirect(url_for('editprofile'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email 
        form.dob.data = current_user.DOB
    return render_template('editprofile.html',image_file=image_file,title='Edit profile',form = form)

@app.route("/projects",methods=['GET','POST'])
@login_required
def projects():
    # form = ProjectForm()
    # projects = Project.query.all()
    return render_template('projects.html')

@app.route("/projects/add_projects",methods=['GET','POST'])
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        post = Project(project_title=form.project_title.data, project_overview=form.project_overview.data, project_url=form.project_url.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Project has been added !!')
        return redirect(url_for('projects'))
    return render_template('add_project.html',form=form)

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
    form = SkillForm()
    # if form.validate_on_submit():
    return render_template('add_skill.html',form = form)

@app.route("/skills",methods=['GET','POST'])
def skills():
    # form = SkillForm()
    # if form.validate_on_submit():
    return render_template('skills.html')