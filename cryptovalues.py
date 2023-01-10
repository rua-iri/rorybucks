import time
import requests
import datetime
import json


def getCryptoValues(apiKey):
    #calculate the timestamp for today and one week ago
    todayDate = datetime.datetime.now()
    sevenDays = datetime.timedelta(days=7)
    lastWeekDate = todayDate - sevenDays

    url = "https://rest.coinapi.io/v1/exchangerate/SQUID/USD/history"
    url += "?period_id=1DAY"
    url += "&time_start=" + str(lastWeekDate).replace(" ", "T")[:19]
    url += "&time_end=" + str(todayDate).replace(" ", "T")[:19]

    headers = apiKey
    res = requests.get(url, headers=headers)
    historicalData = json.loads(res.text)

    dateValue = []

    for dat in historicalData:
        datDate = dat["time_period_start"].find("T")
        timeStart = dat["time_period_start"][:datDate]
        priceStart = dat["rate_open"]
        dateValue.append((timeStart, priceStart))


    return dateValue


# function to get current price of currency 
# and whether it is currently up or down
def getPriceNow():
    nowStamp = int(time.time())
    secondsInDay = 60 * 60 * 24
    yesterdayStamp = nowStamp - secondsInDay

    # concatenate elements to generate the url
    url = "https://api.coingecko.com/api/v3/coins/squid-game/market_chart/range?vs_currency=usd"
    url += "&from=" + str(yesterdayStamp)
    url += "&to=" + str(nowStamp)

    res = requests.get(url)

    priceData = json.loads(res.text)

    # return the price now and 24 hours ago
    return [priceData["prices"][0], priceData["prices"][-1]]

