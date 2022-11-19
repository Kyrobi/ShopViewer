# Third part libraries
from flask import Flask
from flask import render_template # used to interface with html
import mysql.connector

# Included libraries
import time
import sys
import config

# Own functions
from LoadItemList import setUniqueItems

# Own variables
from LoadItemList import listOfItems


app = Flask(__name__)

highestPrice = 0
lowestPrice = 0 
averagePrice = 0

# Keeping track of when to refresh database
NUMBER_OF_SECONDS_IN_DAY = 86400
lastRefreshTime = 0
currentTime = 0

db = mysql.connector.connect(
    host=config.HOST,
    database=config.DATABASE,
    user=config.USER,
    passwd=config.PASSWD
)

cursor = db.cursor()

def getDatabase():
    
    print("0 length. Inserting")
    # Fetches all the items being sold and puts them into list
    cursor.execute("SELECT itemConfig FROM s10829_QuickShop.shops LIMIT 20")
    
    shopList = []
    for shop in cursor:
        shopList.append(shop)
        # print("\n",shop)
        
    setUniqueItems(shopList)
    #print("List length:", len(listOfItems))
    
    
def checkDatabaseQuery():
    # Simple way to check if we need to query the database again.
    # Needed incase lots of user visits the website and breaks the database connection
    global lastRefreshTime
    global currentTime
    
    # Don't reload the list if it's already populated
    if len(listOfItems) == 0:
        getDatabase()
        lastRefreshTime = time.time() # We update the database and set the timer
        return
        
    currentTime = time.time()
    
    # Refresh the database only if 24 hours have passed
    if (currentTime - lastRefreshTime) > NUMBER_OF_SECONDS_IN_DAY:
        listOfItems.clear() # Resetting the items list to redo the set
        getDatabase()
        lastRefreshTime = currentTime
        return




@app.route("/")
def index():
    getDatabase()
    return render_template("index.html",
                        highestPrice=highestPrice,
                        lowestPrice=lowestPrice,
                        averagePrice=averagePrice,
                        listOfItems=listOfItems
                        )


app.run(host="0.0.0.0", port=80)