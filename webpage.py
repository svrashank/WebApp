from flask import Flask,render_template, url_for

app = Flask(__name__)

posts = [{"Name":"Vrashank Shetty","Skills":"Data Cleaning|EDA|Web Scraping ","Experience":"Fresher"},
         {"Name":"Jane Doe","Skills":"Model building|EDA|Web Development","Experience":"4 Years"}
         ]

@app.route("/")
def sign_in():
    return render_template("signin.html")

@app.route("/signup")
def sign_up():
    return render_template("sign_up.html")

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