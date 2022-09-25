
# look at stock over a certain time frame
# determine if it was a good investement and if it makes sense to invest now
# maybe check a few points along this time frame to check if the stock fluctates
# volatility of stock

# RSI
 
import stocks

if __name__ == '__main__':
    loop = True
    while loop:
        print('Pick an option\n Stock info: 1\n Stock eval: 2\n Exit:       3')
        option:int = int(input())
        if option == 1:
            print('Enter the symbol: ',end="")
            symbol = input().upper()
            stock = stocks.get_close(symbol)
            if stock: print(stock)
            else: print(f'No results for {symbol}',end = '\n\n')
        elif option == 2:
            print('Enter the symbol: ',end="")
            symbol = input().upper()
            stock_info = stocks.get_evaluation(symbol)
            print(stock_info)
        elif option == 3:
            loop = False
        else:
            print('Invalid input, try again')
            



# response = requests.get("https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-06-01/2020-06-17?apiKey=7wnIKSRRpIV4ywFOvuWyt4x59nd_dBDM")
# print(response)