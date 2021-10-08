import requests
import sys

URL = "https://asia-southeast2-price-caching.cloudfunctions.net/query-price"
HEADERS = {"Content-Type": "application/json"}


def get_finage_price(symbols):
    payload = {"source": "finage", "symbols": symbols}
    r = requests.post(URL, headers=HEADERS, json=payload)
    r.raise_for_status()

    pxs = r.json()

    if len(pxs) != len(symbols):
        raise Exception("PXS_AND_SYMBOL_LEN_NOT_MATCH")

    return ",".join([str(float(px)) for px in pxs])


if __name__ == "__main__":
    try:
        print(get_finage_price(sys.argv[1:]))
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
