import requests
from datetime import datetime


def BTC():
    response = requests.get('https://www.bitexen.com/api/v1/ticker/BTCTRY/')
    response_json = response.json()
    price_BTC = response_json['data']['ticker']['last_price']
    volume24h_BTC = response_json['data']['ticker']['volume_24h']
    change_24h_BTC = response_json['data']['ticker']['change_24h']
    time = response_json['data']['ticker']['timestamp']
    current_time = datetime.fromtimestamp(float(time)).strftime("%H:%M:%S")
    return price_BTC, volume24h_BTC, change_24h_BTC, current_time

def BTC_info0():
    response = requests.get('https://www.bitexen.com/api/v1/ticker/BTCTRY/')
    response_json = response.json()
    price_BTC = response_json['data']['ticker']['last_price']
    volume24h_BTC = response_json['data']['ticker']['volume_24h']
    change_24h_BTC = response_json['data']['ticker']['change_24h']
    time = response_json['data']['ticker']['timestamp']
    current_time = datetime.fromtimestamp(float(time)).strftime("%H:%M:%S")
    return price_BTC


def ETH():
    response = requests.get('https://www.bitexen.com/api/v1/ticker/ETHTRY/')
    response_json = response.json()
    price_ETH = response_json['data']['ticker']['last_price']
    volume24h_ETH = response_json['data']['ticker']['volume_24h']
    change_24h_ETH = response_json['data']['ticker']['change_24h']
    time = response_json['data']['ticker']['timestamp']
    current_time = datetime.fromtimestamp(float(time)).strftime("%H:%M:%S")
    return price_ETH, volume24h_ETH, change_24h_ETH, current_time


def XRP():
    response = requests.get('https://www.bitexen.com/api/v1/ticker/XRPTRY/')
    response_json = response.json()
    price_XRP = response_json['data']['ticker']['last_price']
    volume24h_XRP = response_json['data']['ticker']['volume_24h']
    change_24h_XRP = response_json['data']['ticker']['change_24h']
    time = response_json['data']['ticker']['timestamp']
    current_time = datetime.fromtimestamp(float(time)).strftime("%H:%M:%S")
    return price_XRP, volume24h_XRP, change_24h_XRP, current_time


def current_btc_usd_price():
    response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
    response_json = response.json()
    price_BTC = response_json['price']
    return price_BTC