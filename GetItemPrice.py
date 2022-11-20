# Standard library
import sys

# Own variables
from LoadItemList import listOfItems
from LoadItemList import listOfAllItems
from LoadItemList import listOfItemPrices # Contains the price of the items

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
    

# Populates the listOfItemPrices list
def populatePrice():
    
    # Loop through the unique list to see which items we need to calculate for
    for i in listOfItems:
        highestPrice = getHighestPrice(i, listOfAllItems)
        lowestPrice = getLowestPrice(i, listOfAllItems)
        
        item = ItemPrice(i ,lowestPrice, 0, highestPrice)
        listOfItemPrices.add(item)
    
    
def getHighestPrice(itemName, listOfAllItems):
    highestValue = -sys.maxsize - 1 
    
    for i in listOfAllItems:
        if i.getName() == itemName:
            if i.getPrice() > highestValue:
                highestValue = i.getPrice()
                
    return highestValue

        

def getLowestPrice(itemName, listOfAllItems):
    lowestValue = sys.maxsize
        
    for i in listOfAllItems:
        if i.getName() == itemName:
            if i.getPrice() < lowestValue:
                lowestValue = i.getPrice()
                
    return lowestValue
        
    
def getAveragePrice(itemName, listOfAllItems):
    print("sd") 
    
# Loop over the unique items list, and find the lowest, highest, and average price for items. Use objects
# getUniqueItemPrice

# Loop over the UniqueItemPrices, and store them into a sqlite database

# Fetch the data from the database and display it

# Search function to find data of individual items

# Validate item name function to clean and convert it to proper database query string