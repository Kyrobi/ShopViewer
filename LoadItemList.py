from typing import List, Set

# Set to prevent duplicates
# Set of strings
listOfItems: Set[str] = set()

# Function to loop over all the items in the database, and put the name of the items in a list
# getUniqueItems
def setUniqueItems(itemsList):
    for item in itemsList:
        
        itemName = formatItemString(item[0])
        itemName = makeProper(itemName)
        
        listOfItems.add(itemName)
        

# Formats the item string into the item name
def formatItemString(itemString):
    
    # Deal with potion format
    if "meta-type: POTION" in itemString:
        tempString = itemString.replace("\n", "").split(" ")[-1]
        potionType = tempString.split("_")[-1]
        
        itemName = "Potion: " + potionType
        return itemName
    
    # Deal with items with display names
    elif "display-name:" in itemString:
        itemName = itemString.replace("\n", "").split(" ")[9]
        return itemName
    
    elif "type: ENCHANTED_BOOK" in itemString:
        itemName = itemString.replace("\n", "").split(" ")[9]
        enchantment = itemString.replace("\n", "").split(" ")[-2]
        enchantLevel = itemString.replace("\n", "").split(" ")[-1]
        # print("\n", itemName + " " + enchantment + " " + enchantLevel)
        
        
        return itemName.replace("_", " ") + " " + enchantment + " " + enchantLevel
        
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
        
        return "Enchant Book - " + StringBuilder
        
        

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
    

# Loop over the unique items list, and find the lowest, highest, and average price for items. Use objects
# getUniqueItemPrice

# Loop over the UniqueItemPrices, and store them into a sqlite database

# Fetch the data from the database and display it

# Search function to find data of individual items

# Validate item name function to clean and convert it to proper database query string