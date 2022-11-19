

def getPrice():
    
    global averagePrice
    global highestPrice
    global lowestPrice
    
    totalPrice = 0
    highestValue = -sys.maxsize - 1 
    lowestValue = sys.maxsize
    counter = 0
    average = 0
    
    cursor.execute("SELECT price FROM s10829_QuickShop.shops")

    
    for i in (cursor):
        totalPrice += i[0]
        counter += 1
        
        #This will find the highest value
        if i[0] > highestValue:
            highestValue = i[0]

        #This will find the lowest value
        if i[0] < lowestValue:
            lowestValue = i[0]
        
        
    average = totalPrice / counter
    averagePrice = round(average, 2)
    
    
    lowestPrice = lowestValue
    highestPrice = highestValue