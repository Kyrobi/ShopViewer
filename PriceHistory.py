import os.path
import sqlite3

# Data
from LoadItemList import listOfItems
from LoadItemList import listOfItemPrices

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
            price_history (rowid INTEGER PRIMARY KEY AUTOINCREMENT, name TINYTEXT, price INTEGER);
            ''')
    
    else:
        print("Database file already exists")    
    
    
# Put like timer or multithread or whatever to schedule
# price history update every 24 hours
def scheduler():
    print("")

# Updates the lists with up-to-date values
# def updateData():
#     getDatabase()

# Write the average price of the item to the database
def addToDB(itemName, price):
    connnection = sqlite3.connect("Price.db")
    cursor = connnection.cursor()
    
    cursor.execute(
        '''
        INSERT INTO price_history (name, price) VALUES ("Bruh", 23)
        '''
    )
    
    connnection.commit()
    
# Fetch the average price of the item from the database
def readFromDB(itemName):
    print("")

# Returns a tuple for all the item's price
def getPriceHistoryForItem(itemName):
    print("")
