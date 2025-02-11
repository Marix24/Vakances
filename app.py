from flask import Flask, render_template, request
import requests
app = Flask(__name__)
import requests
reqjson={}
vakances=[]
text=requests.get(url="https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=7f68f6fc-a0f9-4c31-b43c-770e97a06fda", data=reqjson)
text=text.json()
results=text["result"]
for i in range (len(results)):

    title=results["records"][i]["Vakances nosaukums"]
    link=results["records"][i]["Vakances paplašināts apraksts"]
    text=results["records"][i]["Vakances kategorija"]
    newelement={
            "title":title,
            "link":link,
            "text": text,
        }
    vakances.append(newelement)
@app.route("/")
def index():
    return render_template("index.html", vakances=vakances)

@app.route("/about")
def about():
    return render_template("about.html")