# quickly get stock information
# information you need:
# last close
# average price over time
# standard deviation or something to track how much it fluctuates

import json
from math import sqrt
import requests
from datetime import date

with open('./config.json','r') as openfile:
    json_object = json.load(openfile)
api_key = json_object['api_key']

def get_evaluation(symbol):
    today = date.today()
    response = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{today.replace(year=today.year-1)}/{date.today()}?adjusted=true&sort=asc&apiKey={api_key}')
    if isValidResponse(response):
        results = response.json()['results']
        sum_close = 0
        sum_squared = 0
        high,low = 0,results[0]['l']
        current = results[len(results)-1]['c']
        for result in results:
            sum_close+=result['c']
            if result['h']>high: high = result['h']
            if result['l']<low: low = result['l']
            
        mean = sum_close/len(results)
        
        for result in results:
            sum_squared += pow(mean-result['c'],2)
            
        sigma = sqrt(sum_squared/len(results)) # sigma = standard deviation
        stock_info = f'\nCurrent Price: %.2f\nAverage price: %.2f\nHighest price: %.2f\nLowest Price: %.2f\nStandard Deviation: %.2f\n' %(current,mean,high,low,sigma)
        eval_info = '\nVolatility: '+get_volatility(sigma,mean)+'\n'
        return f'Info on {symbol} for the past year:\n'+stock_info+eval_info
    else:
        return 'Evaluation failed'


def get_close(symbol:str):
    response = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{symbol}/prev?adjusted=true&apiKey={api_key}')
    if isValidResponse(response):
        symbol = response.json()['ticker']
        result = response.json()['results']
        return Stock(symbol, result[0]['c'], result[0]['h'], result[0]['l'])
    else: 
        return None

def get_volatility(volatility, price) -> str: # This doesn't work or the market is just super messed up right now
    if volatility/price-0.0322 >= 0.03: # percentage volatility - average inflation
        return 'High'
    elif volatility/price-0.0322<3 and volatility/price-0.0322 >=2:
        return 'Medium'
    else:
        return 'Low'
        
    

def isValidResponse(response) -> bool: 
    if response.status_code == 200:
        if response.json()['resultsCount']>0: return True
    return False

class Stock():
    def __init__(self, symbol:str, close, high, low):
        self.symbol = symbol
        self.close = close
        self.high = high
        self.low = low 
    def __str__(self):
        return f'\nInfo for {self.symbol}\nLast Close:%9.2f\nHigh:%15.2f\nLow:%16.2f\n' %(self.close, self.high, self.low)
    

    
if __name__ == '__main__':
    print(get_evaluation('AAPL'))
    
