from time import time
import concurrent.futures
import http.client
import sys
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_price(symbol):
    conn = http.client.HTTPSConnection("query2.finance.yahoo.com")
    payload = ""
    headers = {"Content-Type": "application/json"}
    conn.request("GET", "/v8/finance/chart/" + symbol, payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())
    meta = data["chart"]["result"][0]["meta"]

    return meta["regularMarketPrice"]


def get_yfinance_prices(symbols):
    results = dict.fromkeys(symbols)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(symbols)) as executor:
            future_to_symbol = {executor.submit(get_price, symbol): symbol for (symbol) in symbols}
            for future in concurrent.futures.as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    results[symbol] = future.result()
                except Exception as exc:
                    print(f"{symbol} generated an exception: {exc}")

        return results
    except Exception as e:
        print("yfinance: ", e)
        return result
