from flask import Flask, render_template, request

app = Flask(__name__)

vakances=[{
    "title" : "1",
    "text" : "2"
    },{
    "title":"3",
    "text":"4"
    }]
@app.route("/")
def index():
    return render_template("index.html", vakances=vakances)

@app.route("/about")
def about():
    return render_template("about.html")