import binance
from binance.client import Client
import requests
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,url_for
)
app = Flask(__name__)


def get_binance_info():
    client = Client(api_key_binance, api_secret_binance)
    prices = client.get_all_tickers()

    for item in prices:
        if "BTCUSDT" in item["symbol"]:
            btc_price = item["price"]

        if "ETHUSDT" in item["symbol"]:
            eth_price = item["price"]

    return float(btc_price), float(eth_price)

def get_crypto_compare_info():
    btc_url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key=d407a73741e11d9f529b9c721f47143d70b477bc5ac0558a1e0fa5e2c8c77e6b'
    response = requests.get(btc_url)
    btc = response.json()
    btc = btc["USD"]


    eth_url = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD&api_key=d407a73741e11d9f529b9c721f47143d70b477bc5ac0558a1e0fa5e2c8c77e6b'
    response = requests.get(eth_url)
    eth = response.json()
    eth = eth["USD"]

    return btc,eth


@app.route('/')
def hello_world():
    btc_price_binance, eth_price_binance = get_binance_info()
    btc_price_crypto, eth_price_crypto = get_crypto_compare_info()
    ans = []

    #printing value as a table
    items = [["Crypto Compare", "Bitcoin", btc_price_crypto], ["Binance", "Bitcoin", btc_price_binance],
    ["Binance", "Ethereum", eth_price_binance], ["Crypto Compare", "Ethereum", eth_price_crypto]]


    # Print the html



    if btc_price_crypto <= btc_price_binance:
        ans.append("We recommend you buy Bitcoin from CryptoCompare and sell on Binance.")
    else:
        ans.append("We recommend you buy Bitcoin from Binance and sell on CryptoCompare.")

    if eth_price_crypto <= eth_price_binance:
        ans.append(" We recommend you buy Ethereum from CryptoCompare and sell on Binance.")
    else:
        ans.append(" We recommend you buy Ethereum from Binance and sell on CryptoCompare.")

    return render_template('/spell.html',ans=ans,items=items)



if __name__ == '__main__':
    with open('secrets.txt', 'r') as file:
        data = file.read()

    #print(data)

    api_key_binance = data[0]
    api_secret_binance = data[1]

    app.run()
