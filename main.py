from flask import Flask
from flask import render_template # used to interface with html
from flask_mysqldb import MySQL

import mysql.connector
import sys
import config

app = Flask(__name__)

# app.config['MYSQL_USER'] = "u10829_8QYeQRiC7v"
# app.config['MYSQL_PASSWORD'] = "tNXogyKWJkoYzdw12GXv0EG0"
# app.config['MYSQL_HOST'] = "auggie.bloom.host"
# app.config['MYSQL_DB'] = "s10829_QuickShop"
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# mysql = MySQL(app)

user = "fenhrir"

highestPrice = 0
lowestPrice = 0 
averagePrice = 0

db = mysql.connector.connect(
    host=config.HOST,
    database=config.DATABASE,
    user=config.USER,
    passwd=config.PASSWD
)

cursor = db.cursor()

def getDatabase():
    cursor = db.cursor()

    
    #JSON Objects
    #SELECT * FROM s10829_QuickShop.shops WHERE JSON_EXTRACT(owner, "$.owner") = "085c780f-3171-4426-a708-5ea6c7f5321f" LIMIT 10;
    #cursor.execute("SELECT price FROM s10829_QuickShop.shops WHERE JSON_EXTRACT(owner, '$.owner') = '085c780f-3171-4426-a708-5ea6c7f5321f' LIMIT 200")
    cursor.execute("SELECT price FROM s10829_QuickShop.shops LIMIT 20")
    cursor.fetchall()
    
    shopList = []
    
    for shop in cursor:
        shopList.append(shop)
        
    return shopList


def getPrice():
    
    global averagePrice
    global highestPrice
    global lowestPrice
    
    totalPrice = 0
    highestValue = -sys.maxsize - 1 
    lowestValue = sys.maxsize
    counter = 0
    average = 0
    
    cursor.execute("SELECT price FROM s10829_QuickShop.shops")

    
    for i in (cursor):
        totalPrice += i[0]
        counter += 1
        
        #This will find the highest value
        if i[0] > highestValue:
            highestValue = i[0]

        #This will find the lowest value
        if i[0] < lowestValue:
            lowestValue = i[0]
        
        
    average = totalPrice / counter
    averagePrice = round(average, 2)
    
    
    lowestPrice = lowestValue
    highestPrice = highestValue
    

@app.route("/")
def index():
    getPrice()
    return render_template("index.html",
                        highestPrice=highestPrice,
                        lowestPrice=lowestPrice,
                        averagePrice=averagePrice
                        )


app.run(host="0.0.0.0", port=80)