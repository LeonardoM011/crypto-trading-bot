# Crypto trading bot using binance api
# Author: LeonardoM011<Leonardo.leo.201@gmail.com>
# Created on 2021-02-05 21:56

# Set constants here:
DELTA_TIME = 300    # How long can we check for setting up new trade (in seconds)  
# ----------------------

import os
import time
import datetime
import requests
from binance.client import Client



def find_index_of(key, value, list):
    return next((i for i, item in enumerate(list) if item[key] == value), None)

def main():
    api_key = input("Enter BINANCE API KEY (press enter to fetch from env var): ")
    if not api_key:
        print("Trying to fetch from env variable ($BINANCE_API_KEY)...")
        api_key = os.environ.get("BINANCE_API_KEY")
        if not api_key:
            print("Unable to fetch API KEY!")
            return -1
        print("API KEY successfully fetched.")
    
    api_secret = input("Enter BINANCE API SECRET KEY (press enter to fetch from env var): ")
    if not api_secret:
        print("Trying to fetch from env variable ($BINANCE_API_SECRET_KEY)...")
        api_secret = os.environ.get("BINANCE_API_SECRET_KEY")
        if not api_secret:
            print("Unable to fetch API SECRET KEY!")
            return -1
        print("API SECRET KEY successfully fetched.")
    
    print("Connecting to binance...")
    client = Client(api_key, api_secret)

    if (client.get_system_status()['status'] != 0 and client.get_system_status()['msg'] != 'normal'):
        print("Error connecting to binance!")
        return -1
    print("Successfully connected to binance with api key.")

    while True:


        time.sleep(60)
    # datetime.datetime.now().year
    #btcusdt_price = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
    #if (btcusdt_price.status_code != 200):
    #    print("Error connecting to api server to get price")
    #    return
    #print("Successfully connected and got price")

    #while(True):
    #    btcusdt_price = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
    #    print("BTC/USDT: {}".format(btcusdt_price.json()['price']))
    #    time.sleep(1.0)

    #btcusdtindex = find_index_of('symbol', 'BTCUSDT', client.get_all_tickers())
    #while (True):
    #    print(client.get_all_tickers()[btcusdtindex])
    #    time.sleep(5.0)
    # client.futures_create_order(symbol="BTCUSDT", side="SELL", type="STOP", quantity=0.001, price=57975.0, stopPrice=57976.0, workingType="MARK_PRICE")
    # client.futures_create_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.001)
    client.close()

if __name__ == "__main__":
    main()