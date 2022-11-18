from flask import Flask
from flask import render_template # used to interface with html

import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="auggie.bloom.host",
    database="s10829_QuickShop",
    user="u10829_8QYeQRiC7v",
    passwd="tNXogyKWJkoYzdw12GXv0EG0"
)

def getDatabase():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM s10829_QuickShop.shops LIMIT 10")
    
    shopList = []
    
    for shop in cursor:
        shopList.append(shop)
        print(shop)
        
    return shopList
    

@app.route("/")
def index():
    return render_template("index.html", textVariable=getDatabase())


app.run(host="0.0.0.0", port=80)