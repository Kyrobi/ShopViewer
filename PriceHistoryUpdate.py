import sys, config, sqlite3, datetime, os.path, schedule, time, threading
import mysql.connector

class ItemPrice:
    def __init__(self, name, lowestPrice, averagePrice, highestPrice):
        self.name = name
        self.lowestPrice = lowestPrice
        self.averagePrice = averagePrice
        self.highestPrice = highestPrice
    
    def getName(self):
        return self.name
    
    def getLowestPrice(self):
        return self.lowestPrice
    
    def getAveragePrice(self):
        return self.averagePrice
    
    def getHighestPrice(self):
        return self.highestPrice
    
class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    def getPrice(self):
        return self.price
    
    def getName(self):
        return self.name
    

listOfUniqueItems = set()
listOfAllItems = []
listOfItemPrices = set()
    
    
# Populates the list with names of all the available items
def getDatabase():
    
    db = mysql.connector.connect(
    host=config.HOST,
    database=config.DATABASE,
    user=config.USER,
    passwd=config.PASSWD
    )
    
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM s10829_QuickShop.shops")
    
    itemList = []
    for row in cursor:
        itemList.append(row)
        
    db.close()
        
    print(datetime.datetime.now(), " Updating database...")
    setUniqueItems(itemList)
    print(datetime.datetime.now(), " Updated database!")
    
# Function for formatting strings
def setUniqueItems(itemsList):
    
    for item in itemsList:
        
        itemName = formatItemString(item[2]) # Index 2 is the item string in the tuple
        itemName = makeProper(itemName)
        itemPrice = item[1] # Index 1 is the item price    
        
        itemClass = Item(itemName, itemPrice)
        
        listOfUniqueItems.add(itemName) # Add to Set the name of the item
        listOfAllItems.append(itemClass)
        
        
        
    for i in listOfUniqueItems:
        # highestPrice = getHighestPriceForItem(i, listOfAllItems)
        # lowestPrice = getLowestPriceForItem(i, listOfAllItems)
        
        highestPrice = 0
        lowestPrice = 0
        
        averagePrice = getAveragePriceForItem(i, listOfAllItems)
        
        item = ItemPrice(i ,lowestPrice, averagePrice, highestPrice)
        listOfItemPrices.add(item)
        
    
    # We write the prices to the database
    for i in listOfUniqueItems:
        addToDB(i)
    
    
# Formats the item string into the item name
def formatItemString(itemString):
    
    # Deal with potion format
    if "meta-type: POTION" in itemString:
        tempString = itemString.replace("\n", "").split(" ")[-1]
        potionType = tempString.split("_")[-1]
        
        itemName = "Potion: " + potionType
        return itemName
    
    
    # Custom formatting for enchanted books
    if "ENCHANTED_BOOK" in itemString:
        itemName = itemString.replace("\n", "").split(" ")[9]
        enchantment = itemString.replace("\n", "").split(" ")[-2]
        enchantLevel = itemString.replace("\n", "").split(" ")[-1]
        # print("\n", itemName + " " + enchantment + " " + enchantLevel)
        return itemName.replace("_", " ") + " " + enchantment + " " + enchantLevel
    
    
    # Deal with tropical fish buckets
    if "type: TROPICAL_FISH_BUCKET":
        itemName = itemString.replace("\n", "").split(" ")[9]
        return itemName

        
    
    if "meta-type: UNSPECIFIC" in itemString:
        itemName = itemString.replace("\n", "").split(" ")[9]
        return itemName
    
    # For things like shulker boxes / axolotl in buckets
    if "internal: H4sIAAAAAAAA" in itemString:
        itemName = itemString.replace("\n", "").split(" ")[9]
        return itemName
    
    # Deal with items with display names
    if "display-name:" in itemString:
        itemName = itemString.replace("\n", "").split(" ")[9]
        return itemName
    
    
    
        
    # Removes the \n from the string, split into list, and
    # take the last value in the list which is the name
    itemName = itemString.replace("\n", "").split(" ")[-1]
    return itemName


# This function takes an improper string and makes it proper
# i.e. Capitalization, remove underscores, lowercasing, etc
def makeProper(itemName):

    if "ENCHANTED BOOK" in itemName:
        properName = ""
    
        # Strip underscore
        properName = itemName.replace("_", " ")
        properName = properName.replace("ENCHANTED BOOK", "")
        
        # Converts everthing to lowercase
        properName = properName.lower()
        splitString = properName.split(" ")
        
        StringBuilder = ""
        
        for i in splitString:
            StringBuilder += (i.capitalize() + " ")
        
        return "Enchanted Book -" + StringBuilder
    
        
        

    properName = ""
    
    # Strip underscore
    properName = itemName.replace("_", " ")
    
    # Converts everthing to lowercase
    properName = properName.lower()
    splitString = properName.split(" ")
    
    StringBuilder = ""
    
    for i in splitString:
        StringBuilder += (i.capitalize() + " ")
    
    
    return StringBuilder   
    
    
    
    
# def getHighestPriceForItem(itemName, listOfAllItems):
#     highestValue = -sys.maxsize - 1 
    
#     for i in listOfAllItems:
#         if i.getName() == itemName:
#             if i.getPrice() > highestValue:
#                 highestValue = i.getPrice()
                
#     return highestValue

        

# def getLowestPriceForItem(itemName, listOfAllItems):
#     lowestValue = sys.maxsize
        
#     for i in listOfAllItems:
#         if i.getName() == itemName:
#             if i.getPrice() < lowestValue:
#                 lowestValue = i.getPrice()
                
#     return lowestValue
        
    
def getAveragePriceForItem(itemName, listOfAllItems):
    
    sumPrice = 0
    counter = 0
    
    for i in listOfAllItems:
        if i.getName() == itemName:
            sumPrice += i.getPrice()
            counter += 1
            
    averagePrice = sumPrice / counter
    return round(averagePrice, 2) # Round to 2 decimal places


def createPriceHistoryDatabase():
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

createPriceHistoryDatabase() # Creates the database if it doesn't exist
getDatabase()

# Schdules to update the database every 6 hours
# schedule.every(12).hours.do(getDatabase)
def updateScheduleTimer():
    while True:
        schedule.run_pending()
        time.sleep(1)
        
updateScheduleTimer()

# x = threading.Thread(target=updateScheduleTimer)
# x.daemon = True
# x.start()