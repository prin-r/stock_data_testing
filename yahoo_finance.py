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
    regular_period = meta["currentTradingPeriod"]["regular"]
    (regular_time_start, regular_time_end) = (regular_period["start"], regular_period["end"])

    # utc now
    now = int(time())
    if now > int(regular_time_start) and now < int(regular_time_end):
        return meta["regularMarketPrice"]
    else:
        return meta["previousClose"]


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