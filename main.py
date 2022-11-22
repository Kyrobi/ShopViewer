# Third part libraries
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Included libraries
import time
import sys
import config
import logging
import re

# Own functions
from LoadItemList import setUniqueItems
from GetItemPrice import populatePrice
from PriceHistory import createDatabase as createPriceHistoryDatabase

# Own variables
from LoadItemList import listOfItems
from LoadItemList import listOfAllItems
from LoadItemList import listOfItemPrices


app = Flask(__name__)
app.static_folder = 'static'

# Don't log HTTP requests in console
# log = logging.getLogger('werkzeug') # Get Flask's logger
# log.setLevel(logging.ERROR)


# Keeping track of when to refresh database
NUMBER_OF_SECONDS_IN_DAY = 86400
lastRefreshTime = 0
currentTime = 0

# Keeping track of requests to websites
userRequests = []
class User:
    def __init__(self, time):
        self.time = time

db = mysql.connector.connect(
    host=config.HOST,
    database=config.DATABASE,
    user=config.USER,
    passwd=config.PASSWD
)

cursor = db.cursor()

def getDatabase():
    
    # Fetches all the items being sold and puts them into list
    # cursor.execute("SELECT itemConfig FROM s10829_QuickShop.shops LIMIT 10")
    cursor.execute("SELECT * FROM s10829_QuickShop.shops")
    
    shopList = []
    for shop in cursor:
        shopList.append(shop)
        # print("\n",shop)
        
    setUniqueItems(shopList)
    populatePrice()
    
    #print("List length:", len(listOfItems))
    
    
def checkDatabaseQuery():
    # Simple way to check if we need to query the database again.
    # Needed incase lots of user visits the website and breaks the database connection
    global lastRefreshTime
    global currentTime
    
    # Don't reload the list if it's already populated
    if len(listOfItems) == 0:
        # print("Populating empty list")
        getDatabase()
        lastRefreshTime = time.time() # We update the database and set the timer
        return
        
    currentTime = time.time()
    
    # Refresh the database only if 24 hours have passed
    if (currentTime - lastRefreshTime) > NUMBER_OF_SECONDS_IN_DAY:
        # print("Populating list because 24 hours have passed")
        
        # Resetting the lists so they can be repopulated with updated data
        listOfItems.clear()
        listOfAllItems.clear()
        listOfItemPrices.clear()
        
        getDatabase()
        lastRefreshTime = currentTime
        return
    
    # print("Not refreshing list / database")
    
        

@app.route("/", methods=["POST", "GET"])
def index():
    
    # print("Printing price")
    # for i in listOfItemPrices:
    #     print("Item name: ", i.getName(), "  Lowest Price: ", i.getLowestPrice(), " Highest Price: ", i.getHighestPrice())
        
    if request.method == "POST":
        item = request.form["itemInput"]
        print("Input: ", item)
        return redirect(url_for("item", item=item)) # First arg is the function name. Second arg is the parameter for the function
    else:
        return render_template("index.html")
    
    
@app.route("/<item>", methods=["POST", "GET"])
def item(item):
    
    foundItems = []
    
    print("Trying to find:", item) 
    
    for i in listOfItemPrices:
        if re.search(item, i.getName(), re.IGNORECASE): # Deal with casing
            foundItems.append(i)
    
    
    return render_template("displayitem.html",
                        foundItems=foundItems
                        )

checkDatabaseQuery() # Populate the database on page load
createPriceHistoryDatabase() # Creates the database to store price history if it doesn't exist
app.run(host="0.0.0.0", port=80)