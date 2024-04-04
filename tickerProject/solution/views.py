# miscellaneous
import requests

# django imports
from django.core.cache import cache
from django.http import JsonResponse

# model imports
from django.db.models import Min, Max
from .models import StockData

# datatime imports
from datetime import timedelta, datetime

# Create your views here.

# API key: DQXEQ668L7DDUSIF

class Data:
    """
    Created data class to load and store data from api into StockData model (can be found in models.py)
    """
    def get_and_store(self, symbol):

        # get the stock data from the cache
        cacheData = cache.get(symbol)
        if cacheData:
            return cacheData

        # store api key and url and use django requests to get data
        key = 'DQXEQ668L7DDUSIF'
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}'
        r = requests.get(url)
        data = r.json()
        # print data for user to see
        print(data)

        # parse through daily data points and store them in the database
        for dateVal, dailyInfo in data["Time Series (Daily)"].items():
            dateObj = datetime.strptime(dateVal, '%Y-%m-%d').date()
            # update or create a StockData object for each date
            StockData.objects.update_or_create(
                symbol=symbol,
                date=dateObj,
                defaults={
                    'open': dailyInfo["1. open"],
                    'high': dailyInfo["2. high"],
                    'low': dailyInfo["3. low"],
                    'close': dailyInfo["4. close"],
                    'volume': dailyInfo["5. volume"],
                }
            )

        # cachce api response and return the data
        cache.set(symbol, data, timeout=10000) 
        return data

def Lookup(request, symbol, date):
    """
    given a symbol and a date, return the open, high, low, close, and volume for that symbol on that date. Response should be in this format:
    ```json
    { "open":   127.1000, 
    "high":   128.2900,
    "low":    126.5300,
    "close":  127.9600,
    "volume": 3671903 }
    ```
    """
    # call and load data from data class
    getData = Data()
    getData.get_and_store(symbol) 

    try:
        # create new object using stockdata model in models.py
        stockData = StockData.objects.get(symbol=symbol, date=date)
        # store data in json format
        data = {
            "open": stockData.open,
            "high": stockData.high,
            "low": stockData.low,
            "close": stockData.close,
            "volume": stockData.volume
        }
        # return data if found
        return JsonResponse(data, status=200)

    # if data does not exist return error message
    except StockData.DoesNotExist:
        return JsonResponse({"Error": "Data for stock does not exist, try last refreshed date"}, status=400)

def minPrice(request, symbol, n):
    """
    given a symbol and a range 'n', return the lowest price that symbol traded at over the last 'n' data points (lowest low). Response should be in this format:
    ```json
    {"min": 122.685}
    ```
    """
    # call and load data from data class
    getData = Data()
    getData.get_and_store(symbol) 

    # set start and end dates
    endDate = datetime.now().date()
    startDate = endDate - timedelta(days=n)

    # create new object using stockdata model in models.py and filter symbol and range to find specific stock
    minPriceValue = StockData.objects.filter(
        symbol=symbol,
        date__range=[startDate, endDate]
        # use django's min function to find min value from filtered data
    ).aggregate(minLow=Min('low'))

    # if it exists return the value in json format 
    if minPriceValue['minLow'] is not None:
        return JsonResponse({"min": float(minPriceValue['minLow'])}, status=200)
    # if data does not exist return error message
    else:
        return JsonResponse({"Error": "Data for stock does not exist, try last refreshed date"}, status=400)

def maxPrice(request, symbol, n):
    """
    given a symbol and a range 'n', return the highest price that symbol traded at over the last 'n' data points (highest high). Response should be in this format:
    ```json
    {"max": 128.93}
    ```
    """
    # call and load data from data class
    getData = Data()
    getData.get_and_store(symbol) 

    # set start and end dates
    endDate = datetime.now().date()
    startDate = endDate - timedelta(days=n)

    # create new object using stockdata model in models.py and filter symbol and range to find specific stock
    maxPriceValue = StockData.objects.filter(
        symbol=symbol,
        date__range=[startDate, endDate]
        # use django's min function to find min value from filtered data
    ).aggregate(maxHigh=Max('high'))

    # if it exists return the value in json format 
    if maxPriceValue['maxHigh'] is not None:
        return JsonResponse({"max": float(maxPriceValue['maxHigh'])}, status=200)
    # if data does not exist return error message
    else:
        return JsonResponse({"Error": "Data for stock does not exist, try last refreshed date"}, status=400)