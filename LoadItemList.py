from typing import List, Set

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    def getPrice(self):
        return self.price
    
    def getName(self):
        return self.name
        
# Keeps track of the unique names of items - no duplicates
# Used for sorting I guess
listOfItems: Set[Item] = set() 
listOfAllItems: List[Item] = [] # Keeps track of all the items
listOfItemPrices = set() # Stores the prices of the items

# Function to loop over all the items in the database, and put the name of the items in a list
# getUniqueItems
def setUniqueItems(itemsList):
    for item in itemsList:
        
        itemName = formatItemString(item[2]) # Index 2 is the item string in the tuple
        itemName = makeProper(itemName)
        itemPrice = item[1] # Index 1 is the item price
        
        itemClass = Item(itemName, itemPrice)
        
        listOfItems.add(itemName) # Add to Set the name of the item
        listOfAllItems.append(itemClass)
        

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
        
        return "Enchanted Book - " + StringBuilder
        
        

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
    