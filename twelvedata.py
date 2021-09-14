import os
import requests


API_KEY = os.getenv("TWELVEDATA_API_KEY")


def get_price(symbols):
    URL = "https://api.twelvedata.com/price"
    return requests.get(
        URL, params={"symbol": ",".join(symbols), "apikey": API_KEY, "prepost": "true"}, timeout=30
    ).json()


def get_twelvedata_price(symbols):
    try:
        result = get_price(symbols)
        prices = {}

        for symbol in result:
            if "price" in result[symbol]:
                prices[symbol] = result[symbol]["price"]
            else:
                prices[symbol] = None

        return prices
    except Exception as e:
        print("twelvedata: ", e)
        return dict.fromkeys(symbols)
