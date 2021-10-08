#!/usr/bin/env python3
import requests
import json
import sys

URL = "https://app-money.tmx.com/graphql"
HEADERS = {"Content-Type": "application/json"}


def get_tmx_prices(symbols):
    try:
        symbol = symbols[0]
        res = requests.post(
            URL,
            headers=HEADERS,
            data=json.dumps(
                {
                    "operationName": "getQuoteBySymbol",
                    "variables": {"symbol": symbol, "locale": "en"},
                    "query": "query getQuoteBySymbol($symbol: String, $locale: String) {\n  getQuoteBySymbol(symbol: $symbol, locale: $locale) {\n    price\n}\n}\n",
                }
            ),
        )
        return res.json()["data"]["getQuoteBySymbol"]["price"]
    except Exception as e:
        return ",".join(["None"] * len(symbols))


if __name__ == "__main__":
    try:
        print(get_tmx_prices(sys.argv[1:]))
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
