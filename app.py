import binance
from binance.client import Client
import requests
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,url_for
)
import os
from cryptography.fernet import Fernet

app = Flask(__name__)


#function to get info from Binance
def get_binance_info():
    client = Client(api_key_binance, api_secret_binance)
    prices = client.get_all_tickers()

    for item in prices:
        if "BTCUSDT" in item["symbol"]:
            btc_price = item["price"]

        if "ETHUSDT" in item["symbol"]:
            eth_price = item["price"]

    return float(btc_price), float(eth_price)

#function to get info from CryptoCompare
def get_crypto_compare_info():
    btc_url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD'
    data = {'api_key': api_key_crypto_compare}
    response = requests.get(btc_url, data = data)
    btc = response.json()
    btc = btc["USD"]


    eth_url = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'
    response = requests.get(eth_url, data = data)
    eth = response.json()
    eth = eth["USD"]

    return btc,eth


@app.route('/')
#This function is executed when page is loaded
def display_op():
    btc_price_binance, eth_price_binance = get_binance_info()
    btc_price_crypto, eth_price_crypto = get_crypto_compare_info()
    ans = []

    #printing value as a table
    items = [["Crypto Compare", "Bitcoin", btc_price_crypto], ["Binance", "Bitcoin", btc_price_binance],
    ["Binance", "Ethereum", eth_price_binance], ["Crypto Compare", "Ethereum", eth_price_crypto]]



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


    api_key_binance = os.environ['api_key_binance']
    api_secret_binance = os.environ['api_key_binance_2']


    api_key_crypto_compare = os.environ['crypto_keys']
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
