from flask import Flask, render_template, request

import sqlite3, requests
sql_create = """
    CREATE TABLE IF NOT EXISTS vakances (
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

import time
app = Flask(__name__)

reqjson={}
fileavailable=True
vakances=[]
text=requests.get(url="https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=7f68f6fc-a0f9-4c31-b43c-770e97a06fda", data=reqjson)
text=text.json()
results=text["result"]
'''
for i in range (len(results)):

    title=results["records"][i]["Vakances nosaukums"]
    link=results["records"][i]["Vakances paplašināts apraksts"]
    text=results["records"][i]["Vakances kategorija"]
    payfrom=results["records"][i]["Alga no"]
    payto=results["records"][i]["Alga līdz"]
    newelement={
            "title":title,
            "link":link,
            "text": text,
            "payfrom":payfrom,
            "payto":payto
        }
    vakances.append(newelement)
'''
@app.route("/", methods=["POST","GET"])
def index():
    print("execute")
    if request.method=="GET":
        print("getdata")
        vakances=get_data("")
        #print(vakances)
        global fileavailable
        if fileavailable==True:
            fileavailable=False
            file=open("laiki.txt","r+")
            timewr=file.read()
            print(timewr)
            try:
                timewr=float(timewr)
            except:
                timewr=0 #write corrupted time to the valid one
            if(time.time()-timewr>86400):
                file.close()
                "TO DO"
                file=open("laiki.txt","w+")
                fetch_and_store_data()
                file.write(str(time.time()))
            file.close()
            fileavailable=True
    if request.method=="POST":
        print("TODO")
        vakances=get_data("")
        filter1=""
        print(3)
        algano=request.form.get("A1")
        print(4)
        algalidz=request.form.get("A2")
        print(5)
        Vakancesnosaukums=request.form.get("A3")
        print(6)
        Vakanceskategorija=request.form.get("A4")
        print(2)
        try:
            if int(algano)<0:
                algano=0
        except:
            print("err")
            algano=0
        try:
            if int(algalidz)<0:
                algalidz=100000
        except:
            algalidz=100000
        filter1=f'WHERE (nosaukums LIKE "{Vakancesnosaukums}%" AND kategorija LIKE "{Vakanceskategorija}%") AND (algano>={algano} AND algalidz<={algalidz})'
        vakances=get_data(filter1)
        print(1)
        print(vakances)
        
    return render_template("index.html", vakances=vakances)

sql_store = """
    INSERT INTO vakances (vakancesnr, aktdatums, regnr, nosaukums, kategorija, algano, algalidz, slodze, darbalaiks, termins, attels, vieta, apraksts)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);
"""

conn = None
cursor = None
def open_db():
    global conn, cursor
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

def close_db():
    global conn, cursor
    conn.commit()
    conn.close()
    conn = None
    cursor = None
def create_db():
    global conn, cursor
    cursor.execute(sql_create)

def fetch_and_store_data():
    open_db()
    response = requests.get("https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=7f68f6fc-a0f9-4c31-b43c-770e97a06fda")
    data = response.json()
    #print( data )
    rows = data["result"]["records"]
    cursor.execute("DELETE FROM vakances")
    for row in rows:
        #print( (row['NMPP_KODS'], row['NMPP_NOSAUKUMS'], row['NMPP_ADRESE']) )
        cursor.execute(sql_store , (row["Vakances Nr"], row["Aktualizācijas datums"], row["Iestādes reģistrācijas numurs"], row["Vakances nosaukums"], row["Vakances kategorija"], row["Alga no"], row["Alga līdz"], row["Slodzes tips"], row["Darba laika veids"], row["Pieteikšanās termiņš"], row["Attēls"], row["Vieta"], row["Vakances paplašināts apraksts"]))
    close_db()
def get_data( filter1 ):
    sql_get_data = f"""
    SELECT * FROM vakances {filter1};
"""
    open_db()
    create_db()
    #create_tables()
    fetch_and_store_data() #saglabā jaunāko datu versiju no API uz db
    open_db()
    print(sql_get_data)
    cursor.execute( sql_get_data )
    rows = cursor.fetchall()

    close_db()
    return rows
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/filter", methods = ['GET'])
def filter(): 
    filter = request.args.get('filter', default="")
    rows = get_data(filter)
    
    
    
    print(rows)
    return render_template("filter.html", rows = rows)