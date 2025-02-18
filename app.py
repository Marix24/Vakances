from flask import Flask, render_template, request
import sqlite3, requests
sql_create = """
    CREATE TABLE IF NOT EXISTS vakances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vakancesnr INTEGER,
        aktdatums TEXT,
        regnr TEXT,
        nosaukums TEXT,
        kategorija TEXT,
        algano INTEGER,
        algalidz INTEGER,
        slodze TEXT,
        darbalaiks TEXT,
        termins TEXT,
        attels TEXT,
        vieta TEXT,
        apraksts TEXT  
    );
"""
sql_store = """
    INSERT INTO vakances (id, vakancesnr, aktdatums, regnr, nosaukums, kategorija, algano, algalidz, slodze, darbalaiks, termins, attels, vieta, apraksts)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
"""
def create_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(sql_create)
    conn.commit()
    conn.close()
def fetch_and_store_data():
    response = requests.get("https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=7f68f6fc-a0f9-4c31-b43c-770e97a06fda")
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM punkti")
    data = response.json()
    #print( data )
    rows = data["result"]["records"]
    conn = sqlite3.connect("data.db")
    cursor.execute("DELETE FROM punkti")

    for row in rows:
        #print( (row['NMPP_KODS'], row['NMPP_NOSAUKUMS'], row['NMPP_ADRESE']) )
        cursor.execute( sql_store, (row["_id"], row["Vakances Nr"], row["Aktualizācijas datums"], row["Iestādes reģistrācijas numurs"], row["Vakances nosaukums"], row["Vakances kategorija"], , row["Alga no"], row["Alga līdz"], row["Slodzes tips"], row["Darba laika veids"], row["Pieteikšanās termiņš"], row["Attēls"], row["Vieta"], row["Vakances paplašināts apraksts"]) )
    conn.commit()
    conn.close()
    

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
@app.route("/test")
def test():
    print(ok)
    create_db()
    fetch_and_store_data()
