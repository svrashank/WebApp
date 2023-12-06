from Portfolio import app 
from Portfolio.forms import LoginForm,RegistrationForm 
from flask import render_template, url_for,flash,redirect,request



posts = [{"Name":"Vrashank Shetty","Skills":"Data Cleaning|EDA|Web Scraping ","Experience":"Fresher"},
         {"Name":"Jane Doe","Skills":"Model building|EDA|Web Development","Experience":"4 Years"}
         ]

@app.route("/",methods=['GET','POST'])
def sign_in():
    form  = LoginForm()
    if form.validate_on_submit():
        if form.email.data =='svrashank@gmail.com' and form.password.data =='1234':
            flash(f"Login successful for {form.email.data}",'success')
            return redirect(url_for('home'))
        else:
            if request.method == 'POST':
                flash("Wrong email or password,please try again")
    return render_template("signin.html",title = "Login",form = form)

@app.route("/signup",methods=['GET','POST'])
def sign_up():  
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}",'success')
        return redirect(url_for('home'))
    if request.method == "POST":
        flash("Account not created.Please check your inputs.", 'danger')
    return render_template("sign_up.html",title ="Sign Up",form = form)

@app.route("/qualifications")
def qualifications():
    return render_template("qualifications.html")
 
@app.route("/home")
def home():
    return render_template("home.html",posts=posts)

@app.route("/yourprofile")
def yourprofile():
    return render_template('yourprofile.html')

@app.route("/projects")
def projects():
    return render_template('projects.html')

@app.route("/other interests")
def other_interests():
    return render_template('other_interests.html')