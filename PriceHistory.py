import os.path
import sqlite3
import time
import datetime

# Data
from LoadItemList import listOfItems
from LoadItemList import listOfAllItems
from LoadItemList import listOfItemPrices

from GetItemPrice import getAveragePriceForItem



# Put like timer or multithread or whatever to schedule
# price history update every 24 hours
def priceCheckScheduler():
    print("Calling Scheduler")
    print(str(datetime.datetime.now()) + " Udating price history!")
    updateData()
    
    
# Functions
# from main import getDatabase   
    

# Updates the lists with up-to-date values
def updateData():
    for i in listOfItems:
        addToDB(i)

# Write the average price of the item to the database
def addToDB(itemName):
    connection = sqlite3.connect("Price.db")
    cursor = connection.cursor()
    
    #currenttime = int(time.time())
    currenttime = datetime.datetime.now().date()
    averagePrice = getAveragePriceForItem(itemName, listOfAllItems) 
    
    
    cursor.execute("INSERT INTO price_history (name, time, price) VALUES (?,?,?);", (itemName, currenttime, averagePrice))
    
    connection.commit()
    connection.close()
    

# Returns a tuple for all the item's price
def getPriceHistoryForItem(itemName):
    
    connection = sqlite3.connect("Price.db")
    cursor = connection.cursor()
    
    # Debug
    connection.set_trace_callback(print)
    
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
        
    connection.close()
        
    return times, prices
    
    
    
# createDatabase()
# addToDB("Dirt")
# getPriceHistoryForItem("a")
