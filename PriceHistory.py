import os.path
import sqlite3
import time
import datetime

# Data
from LoadItemList import listOfItems
from LoadItemList import listOfAllItems
from LoadItemList import listOfItemPrices

from GetItemPrice import getAveragePriceForItem
# from main import getDatabase


# Functions
# from main import getDatabase

def createDatabase():
    # Create a new database it one doesn't exists
    if not os.path.isfile("Price.db"):
        print("Database file doesn't exit. Creating a new one")
        connnection = sqlite3.connect("Price.db")
        cursor = connnection.cursor()
        
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS 
            price_history (rowid INTEGER PRIMARY KEY AUTOINCREMENT, name TINYTEXT, time DATE, price INTEGER);
            ''')  
    else:
        print("Database file already exists")    
    
    
# Put like timer or multithread or whatever to schedule
# price history update every 24 hours
def priceCheckScheduler():
    print("")
    # updateData()
    

# Updates the lists with up-to-date values
def updateData():
    print("")
    # getDatabase()
    
    # for i in listOfItems:
    #     addToDB(i.getName())

# Write the average price of the item to the database
def addToDB(itemName):
    connnection = sqlite3.connect("Price.db")
    cursor = connnection.cursor()
    
    #currenttime = int(time.time())
    currenttime = datetime.datetime.now().date()
    # averagePrice = getAveragePriceForItem(itemName, listOfAllItems) 
    averagePrice = 2
    
    
    cursor.execute("INSERT INTO price_history (name, time, price) VALUES (?,?,?);", (itemName, currenttime, averagePrice))
    
    connnection.commit()
    

# Returns a tuple for all the item's price
def getPriceHistoryForItem(itemName):
    
    connnection = sqlite3.connect("Price.db")
    cursor = connnection.cursor()
    
    # Debug
    connnection.set_trace_callback(print)
    
    currentTime = datetime.datetime.now().date()
    pastTime = datetime.datetime.now() - datetime.timedelta(30)
    
    # averagePrice = 0
    
    #cursor.execute("SELECT name,time,price FROM price_history WHERE time <= ? AND time >= ? ORDER BY DESC;", (currentTime, pastTime.date()))
    cursor.execute("SELECT time,price FROM price_history WHERE time BETWEEN ? AND ? AND name=?;", (pastTime.date(), currentTime, itemName))
    
    prices = []
    times = []
    
    # (time, price)
    for i in cursor:
        prices.append(i[1])
        times.append(i[0])
        print(i)
        
    return times, prices
    
    
    
# createDatabase()
# addToDB("Dirt")
# getPriceHistoryForItem("a")
