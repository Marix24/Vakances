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
sql_store = """
    INSERT INTO vakances (vakancesnr, aktdatums, regnr, nosaukums, kategorija, algano, algalidz, slodze, darbalaiks, termins, attels, vieta, apraksts)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);
"""
sql_get_data = """
    SELECT * FROM vakances;
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
    response = requests.get("https://data.gov.lv/dati/lv/api/3/action/datastore_search?resource_id=7f68f6fc-a0f9-4c31-b43c-770e97a06fda")
    data = response.json()
    #print( data )
    rows = data["result"]["records"]
    cursor.execute("DELETE FROM vakances")

    for row in rows:
        #print( (row['NMPP_KODS'], row['NMPP_NOSAUKUMS'], row['NMPP_ADRESE']) )
        cursor.execute(sql_store , (row["Vakances Nr"], row["Aktualizācijas datums"], row["Iestādes reģistrācijas numurs"], row["Vakances nosaukums"], row["Vakances kategorija"], row["Alga no"], row["Alga līdz"], row["Slodzes tips"], row["Darba laika veids"], row["Pieteikšanās termiņš"], row["Attēls"], row["Vieta"], row["Vakances paplašināts apraksts"]))
def get_data( filter ):
    open_db()
    create_db()
    #create_tables()
    fetch_and_store_data() #saglabā jaunāko datu versiju no API uz db

    cursor.execute( sql_get_data )
    rows = cursor.fetchall()

    close_db()
    return rows

    

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/filter", methods = ['GET'])
def filter(): 
    filter = request.args.get('filter', default="")
    rows = get_data(filter)
    
    
    
    print(rows)
    return render_template("filter.html", rows = rows)