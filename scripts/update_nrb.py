#!/usr/bin/env python3
"""Fetch Nepal Rastra Bank's published forex rates and write data/nrb-rates.json.

Fails closed: if the request fails or the data does not pass validation, the
existing file is left untouched and the script exits with a non-zero status
(so the GitHub Action turns red). It never invents or estimates a rate.

NRB_API_BASE can be overridden for testing.
"""
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = os.environ.get("NRB_API_BASE", "https://www.nrb.org.np/api/forex/v1/rates")
OUT = os.environ.get("NRB_OUT", os.path.join(os.path.dirname(__file__), "..", "data", "nrb-rates.json"))
NPT = dt.timezone(dt.timedelta(hours=5, minutes=45))
LOOKBACK_DAYS = 7


def fetch_day(day):
    q = urllib.parse.urlencode({"from": day, "to": day, "per_page": 100, "page": 1})
    req = urllib.request.Request(BASE + "?" + q, headers={"User-Agent": "thenepal.io-rates-updater (+https://converter.thenepal.io)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def num(v):
    try:
        f = float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return None
    return f if f > 0 and f < 1e9 else None


def extract(doc):
    """Return (date, published_on, rates) from the API response, or raise ValueError."""
    days = (doc.get("data") or {}).get("payload") or doc.get("payload") or []
    if not days:
        raise ValueError("no payload")
    day = days[0]
    rates = []
    for r in day.get("rates") or []:
        cur = r.get("currency") or {}
        iso, unit, buy, sell = str(cur.get("iso3", "")).upper(), num(cur.get("unit")), num(r.get("buy")), num(r.get("sell"))
        if len(iso) != 3 or not iso.isalpha() or unit is None or buy is None or sell is None:
            continue  # skip rows that are not complete
        rates.append({"iso3": iso, "name": str(cur.get("name", iso))[:60], "unit": int(unit), "buy": buy, "sell": sell})
    return day.get("date"), day.get("published_on"), rates


def validate(date, rates):
    if not date or not isinstance(date, str):
        raise ValueError("missing date")
    dt.date.fromisoformat(date[:10])
    if len(rates) < 10:
        raise ValueError("too few currencies: %d" % len(rates))
    usd = next((r for r in rates if r["iso3"] == "USD"), None)
    if not usd:
        raise ValueError("USD missing")
    per_unit = usd["buy"] / usd["unit"]
    if not (50 <= per_unit <= 500):
        raise ValueError("USD rate out of plausible range: %s" % per_unit)
    for r in rates:
        if r["sell"] < r["buy"] * 0.5 or r["sell"] > r["buy"] * 2:
            raise ValueError("buy/sell implausible for " + r["iso3"])


def main():
    today = dt.datetime.now(NPT).date()
    last_err = None
    for back in range(LOOKBACK_DAYS):
        day = (today - dt.timedelta(days=back)).isoformat()
        try:
            date, published, rates = extract(fetch_day(day))
            validate(date, rates)
        except Exception as e:  # noqa: BLE001 - any failure means "try the previous day"
            last_err = "%s: %s" % (day, e)
            continue
        out = {
            "source": "Nepal Rastra Bank",
            "source_url": "https://www.nrb.org.np/forex/",
            "date": date[:10],
            "published_on": published,
            "fetched_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "rates": sorted(rates, key=lambda r: r["iso3"]),
        }
        os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
        tmp = OUT + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        os.replace(tmp, OUT)
        print("wrote %s: %d currencies for %s" % (os.path.basename(OUT), len(rates), date[:10]))
        return 0
    print("No valid NRB rates found in the last %d days (%s). File left unchanged." % (LOOKBACK_DAYS, last_err), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
