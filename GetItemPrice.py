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
        highestPrice = getHighestPriceForItem(i, listOfAllItems)
        lowestPrice = getLowestPriceForItem(i, listOfAllItems)
        averagePrice = getAveragePriceForItem(i, listOfAllItems)
        
        item = ItemPrice(i ,lowestPrice, averagePrice, highestPrice)
        listOfItemPrices.add(item)
    
    
def getHighestPriceForItem(itemName, listOfAllItems):
    highestValue = -sys.maxsize - 1 
    
    for i in listOfAllItems:
        if i.getName() == itemName:
            if i.getPrice() > highestValue:
                highestValue = i.getPrice()
                
    return highestValue

        

def getLowestPriceForItem(itemName, listOfAllItems):
    lowestValue = sys.maxsize
        
    for i in listOfAllItems:
        if i.getName() == itemName:
            if i.getPrice() < lowestValue:
                lowestValue = i.getPrice()
                
    return lowestValue
        
    
def getAveragePriceForItem(itemName, listOfAllItems):
    
    sumPrice = 0
    counter = 0
    
    for i in listOfAllItems:
        if i.getName() == itemName:
            sumPrice += i.getPrice()
            counter += 1
            
    averagePrice = sumPrice / counter
    return round(averagePrice, 2) # Round to 2 decimal places
            