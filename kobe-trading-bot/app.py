#!/usr/bin/env python3

# Crypto trading bot using binance api
# Author: LeonardoM011<Leonardo.leo.201@gmail.com>
# Created on 2021-02-05 21:56

# Set constants here:
DELTA_TIME = 300    # How long can we check for setting up new trade (in seconds)  
# ----------------------

# Imports:
import os
import sys
import time as t
import datetime

# Adding python-binance to path and importing python-binance
sys.path.insert(1, "../deps/binance")
from binance.client import Client

from fun import *
import candles as can

# Globals:
client = None

# Main program loop
def start():
    hour_repeated = -1
    try:
        while True:
            time = datetime.datetime.now()
            hour = time.hour
            minute = time.minute
            open_trade = client.futures_get_open_orders()
            if minute < 10:
                if not open_trade and hour_repeated != hour:
                    candles = client.futures_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, contractType="PERPETUAL")
                    info = can.get_candle_info(candles[:-1])
                    candle_side = can.get_side(info)
                    if candle_side:
                        output.print_info('Initiating trade...')
                        #current_price = client.futures_mark_price(symbol="BTCUSDT", contractType="PERPETUAL")['markPrice']
                        close_price = candles
                        client.futures_create_order(symbol="BTCUSDT", side=candle_side, type=Client.ORDER_TYPE_MARKET, quantity=0.001)
                        client.futures_create_order(symbol="BTCUSDT", side=can.flip_side(candle_side), type=Client.ORDER_TYPE_STOP_LOSS_LIMIT, quantity=0.001, price=57975.0, stopPrice=57976.0, workingType="MARK_PRICE")

                    hour_repeated = hour

            t.sleep(300)
    except KeyboardInterrupt:
        print('Program canceled...')

def connect():
    while True:
        api_key = get_api_key("BINANCE_API_KEY")
        api_secret = get_api_key("BINANCE_API_SECRET_KEY")
        
        output.print_info('Connecting to binance...')
        global client 
        client = Client(api_key, api_secret)

        if check_connectivity(client):
            output.print_ok('Successfully connected to binance.')

        if check_account_status(client):
            output.print_ok('Successfully connected using api keys.')
            return

        output.print_failed('Cannot connect to binance with api keys.')

def main():
    output.print_ok('Starting kobe trading bot...')
    
    connect()
    start()

    #try:
    #   client.get_all_orders()
    #except BinanceAPIException as e:
    #   print e.status_code
    #   print e.message
    
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

if __name__ == "__main__":
    main()