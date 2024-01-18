from flask import Blueprint
from Portfolio import db,bcrypt 
import flask 
from Portfolio.users.forms import LoginForm,RegistrationForm 
from flask import render_template, url_for,flash,redirect,request
from Portfolio.models import User,Project,Skills,Qualifications
from flask_login import login_user,current_user,login_required
from Portfolio.users.utils import is_safe_url

users_blueprint = Blueprint('users_blueprint',__name__)

@users_blueprint.route("/",methods=['GET','POST'])
def sign_in():
    if current_user.is_authenticated:
        flash(f"logged in as {current_user.username}")
        return redirect(url_for("main.home"))
    form  = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f"Login successful for {form.email.data}",'success')
            next = request.args.get('next')
            if next and not is_safe_url(next):
                return flask.abort(400)
            return redirect(next or url_for('main.home')) 
        else:
            flash("Wrong email or password,please try again",'error')
    return render_template("signin.html",title = "Login",form = form)




@users_blueprint.route("/signup",methods=['GET','POST'])
def sign_up():  
    if current_user.is_authenticated:
        flash(f"logged in as{current_user.username}")
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Hash Password and store all information in the database 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data.strip(),email = form.email.data.strip(),password = hashed_password)
        # users_blueprint.app_context().push()
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}",'success')
        return redirect(url_for('main.home'))
    if request.method == "POST":
        # for field,error in form.errors.items():
        #     flash(error [0], f'danger_{field}')
        # else:
        #     flash("Account not created. Please check your inputs.", 'danger')
        return render_template("sign_up.html",title ="Sign Up",form = form)

    return render_template("sign_up.html",title ="Sign Up",form = form)

@users_blueprint.route('/show_signup')
def show_sign_up():
    return render_template("sign_up.html", title="Sign Up", form=RegistrationForm())

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
    
@users_blueprint.route("/editprofile/<int:user_id>/delete",methods = ["GET","POST"])
@login_required
def delete_account(user_id):
    # user_id = current_user.id
    delete_user(user_id)
    return redirect(url_for('users_blueprint.sign_up'))