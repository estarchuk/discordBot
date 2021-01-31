from yahoo_fin import stock_info
import requests as req
import json

# CRYTPO KEY 45ebf01e-f601-420a-901d-9e016a0f98ef
url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '45ebf01e-f601-420a-901d-9e016a0f98ef',
}

# TODO: Automatic currency conversion from USD to CAD
# Also needs to grab Ethereum from Crypto exchange, not yahoo-fin

session = req.Session()
session.headers.update(headers)

def getStonk(s):

    f = open('stonkNames.txt', 'r')
    symbols = f.read().splitlines()

    for symbol in symbols:
        if symbol == s:
            price = stock_info.get_live_price(s)
            crypto = False
            return [price, crypto]

    parameters = {
        'amount': '1',
        'symbol': s,
        'convert': 'CAD'
    }

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    crypto = True
    return [data, crypto]




