import os
import csv
import time

from USA.twelvedata import get_twelvedata_price as usa_twelve
from USA.yahoo_finance import get_yfinance_prices as usa_yahoo
from USA.finage import get_finage_price as usa_finage
from USA.bb import get_bb_price as usa_bb

from CAD.bb import get_bb_price as cad_bb
from CAD.finage import get_finage_price as cad_finage
from CAD.tmx import get_tmx_prices as cad_tmx
from CAD.yahoo_finance import get_yfinance_prices as cad_yahoo

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

SYMBOLS_CAD = ["GLXY"]

# if os.getenv("TWELVEDATA_API_KEY") is None or os.getenv("FINAGE_API_KEY") is None:
#     raise ValueError("Please setup TWELVEDATA_API_KEY and FINAGE_API_KEY")


def parse_to_list(price_str):
    return price_str.split(",")


while True:
    ask_time = int(time.time())
    print("start at ", ask_time)

    twelvedata_prices = parse_to_list(usa_twelve(SYMBOLS))
    finage_prices = parse_to_list(usa_finage((SYMBOLS)))
    yfinance_prices = parse_to_list(usa_yahoo(SYMBOLS))
    bb_prices = parse_to_list(usa_bb(SYMBOLS))
    # print(twelvedata_prices)
    # print(finage_prices)
    # print(yfinance_prices)
    # print(bb_prices)

    cad_bb_prices = cad_bb(SYMBOLS_CAD)
    cad_finage_prices = cad_finage((SYMBOLS_CAD))
    caD_tmx_prices = cad_tmx(SYMBOLS_CAD)
    caD_yfinance_prices = cad_yahoo(SYMBOLS_CAD)
    # print(cad_bb_prices)
    # print(cad_finage_prices)
    # print(caD_tmx_prices)
    # print(caD_yfinance_prices)

    for idx, symbol in enumerate(SYMBOLS):
        with open("./reports/" + symbol + ".csv", "a+", encoding="UTF8") as f:
            writer = csv.writer(f)

            # header = ["timestamp", "twelvedata", "finage", "yahoo_finance", "bb"]
            # writer.writerow(header)

            # write the data
            data = [
                ask_time,
                twelvedata_prices[idx],
                finage_prices[idx],
                yfinance_prices[idx],
                bb_prices[idx],
            ]
            writer.writerow(data)

    for idx, symbol in enumerate(SYMBOLS_CAD):
        with open("./reports/" + symbol + ".csv", "a+", encoding="UTF8") as f:
            writer = csv.writer(f)

            # header = ["timestamp", "bb", "finage", "tmx","yahoo_finance"]
            # writer.writerow(header)

            # write the data
            data = [
                ask_time,
                cad_bb_prices,
                cad_finage_prices,
                caD_tmx_prices,
                caD_yfinance_prices,
            ]
            writer.writerow(data)

    print("save and sleep for 1 min")
    time.sleep(60)
