# Third part libraries
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Included libraries
import time, schedule, sqlite3, threading, datetime, logging, sys, string



app = Flask(__name__)
app.static_folder = 'static'

# Don't log HTTP requests in console
# log = logging.getLogger('werkzeug') # Get Flask's logger
# log.setLevel(logging.ERROR)

        
listOfItems = []

def getListOfItems():
    print("Getting list of items...")
    listOfItems.clear()
    connection = sqlite3.connect("Price.db")
    cursor = connection.cursor()
    
    # Debug
    # connection.set_trace_callback(print)
    
    currentTime = datetime.datetime.now().date()
    pastTime = datetime.datetime.now() - datetime.timedelta(90)
    
    cursor.execute("SELECT DISTINCT name FROM price_history WHERE time BETWEEN ? AND ?;", (pastTime.date(), currentTime))
    
    # (time, price)
    for i in cursor:
        listOfItems.append(i[0])
        
    connection.close()
    print("Finished getting list of items...")
    
    
def getPriceHistoryForItem(itemName):
    
    connection = sqlite3.connect("Price.db")
    cursor = connection.cursor()
    
    # Debug
    # connection.set_trace_callback(print)
    
    currentTime = datetime.datetime.now().date()
    pastTime = datetime.datetime.now() - datetime.timedelta(90)
    
    cursor.execute("SELECT time,price FROM price_history WHERE time BETWEEN ? AND ? AND name=?;", (pastTime.date(), currentTime, itemName))
    
    prices = []
    times = []
    
    # (time, price)
    for i in cursor:
        prices.append(i[1])
        times.append(i[0])
        # print(i)
        
    connection.close()
        
    return times, prices

        
        

@app.route("/", methods=["POST", "GET"])
def index():
    
    # print("Printing price")
    # for i in listOfItemPrices:
    #     print("Item name: ", i.getName(), "  Lowest Price: ", i.getLowestPrice(), " Highest Price: ", i.getHighestPrice())
        
    if request.method == "POST":
        item = request.form["itemInput"]
        
        if item == "favicon.ico":
           return render_template("index.html", listOfItems=listOfItems) 
       
        print("Input: ", item)
        return redirect(url_for("item", item=item)) # First arg is the function name. Second arg is the parameter for the function
    else:
        return render_template("index.html", listOfItems=listOfItems)
    
    
    
@app.route("/<item>", methods=["POST", "GET"])
def item(item):
    
    if item == "favicon.ico":
        return render_template("displayitem.html")
    
    item = (str(item)).rstrip()
    item = string.capwords(item)
    item = item + " "
    
    if item in listOfItems: 
        times, prices = getPriceHistoryForItem(item)
        
        # Find the average prices of items in the past 30 days
        sumPrice = 0
        
        highestValue = -sys.maxsize - 1 
        lowestValue = sys.maxsize
        
        for i in prices:
            sumPrice += i
            
            # Get highest price
            if i > highestValue:
                highestValue = i
                
            # Get lowest price
            if i < lowestValue:
                lowestValue = i
            
        averagePriceIn90Days = sumPrice / len(prices)
        
        
        return render_template("displayitem.html",
                            itemName=item,
                            times=times,
                            prices=prices,
                            listOfItems=listOfItems,
                            averagePriceIn90Days=averagePriceIn90Days,
                            highestValue=highestValue,
                            lowestValue=lowestValue,
                            )
    
    else:
        item = item + " does not exist"
        averagePriceIn90Days = "?"
        lowestValue = "?"
        highestValue = "?"
        times = 0
        prices = 0
        return render_template("displayitem.html",
                            itemName=item,
                            times=times,
                            prices=prices,
                            listOfItems=listOfItems,
                            averagePriceIn90Days=averagePriceIn90Days,
                            highestValue=highestValue,
                            lowestValue=lowestValue,
                            )
    

getListOfItems()

schedule.every(6).hours.do(getListOfItems)

def updateScheduleTimer():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.run_pending()

x = threading.Thread(target=updateScheduleTimer)
x.daemon = True
x.start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=25580)