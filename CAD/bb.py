import requests
import sys

headers = {
    "authority": "www.bloomberg.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "user-agent": "Chrome/94.0.4606.61",
}

params = (
    ("locale", "en"),
    ("customTickerList", "true"),
)


def get_bb_price(symbols):
    try:
        r = requests.get(
            "https://www.bloomberg.com/markets2/api/datastrip/{}".format(
                ",".join([s + ":CN" for s in symbols])
            ),
            headers=headers,
            params=params,
        )
        r.raise_for_status()

        rj = r.json()
        pxs = [p["price"] for p in rj]

        if len(pxs) != len(symbols):
            raise Exception("PXS_AND_SYMBOL_LEN_NOT_MATCH")

        return ",".join([str(float(px)) for px in pxs])
    except Exception as e:
        return ",".join(["None"] * len(symbols))


if __name__ == "__main__":
    try:
        print(get_bb_price(sys.argv[1:]))
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
