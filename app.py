from flask import Flask, render_template, request

app = Flask(__name__)

vakances=[{
    "title" : "1",
    "text" : "2",
    "link":"https://www.w3schools.com"
    },{
    "title":"3",
    "text":"4",
    "link":"https://www.w3schools.com"
    }]
@app.route("/")
def index():
    return render_template("index.html", vakances=vakances)

@app.route("/about")
def about():
    return render_template("about.html")