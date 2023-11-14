from flask import Flask,render_template, url_for

app = Flask(__name__)


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/qualifications")
def explanations():
    return render_template("qualifications.html")


@app.route("/browse")
def browse():
    return render_template("browse.html")