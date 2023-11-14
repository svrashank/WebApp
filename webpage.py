from flask import Flask,render_template

app = Flask(__name__)
posts = [{"Project_Name":"Mumbai Weather",
          "Modules":"sklearn, matplotlib, Pandas",
          "Summary":"Shows how the weather has changed over last 3 decades"},

          {"Project_Name":"Webscraping Finances of Companies",
          "Modules":"Requests, BeautifulSoup, Pandas",
          "Summary":"Webscraping major financial indicators of Nifty 50 companies from Yahoo Finance"}]

@app.route("/projects")
def projects():
    return render_template("home.html",posts = posts)

@app.route("/explanations")
def explanations():
    return render_template("explanations.html")
