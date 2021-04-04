import os, time
import requests
from binance.client import Client

def find_index_of(key, value, list):
    return next((i for i, item in enumerate(list) if item[key] == value), None)

def main():
    # You have to set your env variables with your private and public api key or just set it here #
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET_KEY")
    ###############################################################################################
    client = Client(api_key, api_secret)

    if (client.get_system_status()['status'] != 0 and client.get_system_status()['msg'] != 'normal'):
        print("Error connecting to binance with api key")
        return
    print("Successfully connected to binance with api key")

    btcusdt_price = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
    if (btcusdt_price.status_code != 200):
        print("Error connecting to api server to get price")
        return
    print("Successfully connected and got price")

    while(True):
        btcusdt_price = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        print("BTC/USDT: {}".format(btcusdt_price.json()['price']))
        time.sleep(1.0)

    #btcusdtindex = find_index_of('symbol', 'BTCUSDT', client.get_all_tickers())
    #while (True):
    #    print(client.get_all_tickers()[btcusdtindex])
    #    time.sleep(5.0)


if __name__ == "__main__":
    main()