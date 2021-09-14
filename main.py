import os
import csv
import time

from twelvedata import get_twelvedata_price
from yahoo_finance import get_yfinance_prices
from finage import get_finage_price

SYMBOLS = [
    "AAPL",
    "GOOGL",
    "TSLA",
    "NFLX",
    "QQQ",
    "TWTR",
    "BABA",
    "IAU",
    "SLV",
    "USO",
    "VIXY",
    "AMZN",
    "MSFT",
    "FB",
    "GS",
    "ABNB",
    "GME",
    "AMC",
    "SPY",
    "COIN",
    "ARKK",
    "SQ",
    "AMD",
    "HOOD",
]


header = ["timestamp", "twelvedata", "finage", "yahoo_finance"]

if os.getenv("TWELVEDATA_API_KEY") is None or os.getenv("FINAGE_API_KEY") is None:
    raise ValueError("Please setup TWELVEDATA_API_KEY and FINAGE_API_KEY")

while True:
    ask_time = int(time.time())
    print("start at ", ask_time)

    twelvedata_prices = get_twelvedata_price(SYMBOLS)
    finage_prices = get_finage_price((SYMBOLS))
    yfinance_prices = get_yfinance_prices(SYMBOLS)
    # print(twelvedata_prices)
    # print(finage_prices)
    # print(yfinance_prices)

    for symbol in SYMBOLS:
        with open("./reports/" + symbol + ".csv", "a+", encoding="UTF8") as f:
            writer = csv.writer(f)

            # write the header
            # writer.writerow(header)

            # write the data
            data = [ask_time, twelvedata_prices[symbol], finage_prices[symbol], yfinance_prices[symbol]]
            writer.writerow(data)

    print("save and sleep for 1 min")
    time.sleep(60)
