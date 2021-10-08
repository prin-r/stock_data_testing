#!/usr/bin/env python3
from time import time
import concurrent.futures
import http.client
import sys
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_price_single(symbol):
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
            future_to_symbol = {
                executor.submit(get_price_single, symbol): symbol for (symbol) in symbols
            }
            for future in concurrent.futures.as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    results[symbol] = future.result()
                except Exception as exc:
                    print(f"{symbol} generated an exception: {exc}")

        return ",".join([str(results[s]) for s in results])
    except Exception as e:
        return ",".join(["None"] * len(symbols))


if __name__ == "__main__":
    try:
        print(get_yfinance_prices(sys.argv[1:]))
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
