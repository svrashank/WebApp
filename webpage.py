from flask import Flask,render_template, url_for

app = Flask(__name__)


@app.route("/")
def signup():
    return render_template("signin.html")

@app.route("/qualifications")
def explanations():
    return render_template("qualifications.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/yourprofile")
def yourprofile():
    return render_template('yourprofile.html')