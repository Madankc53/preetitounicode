#!/usr/bin/env python3
"""Fetch the daily gold and silver rate published by FENEGOSIDA (Federation of Nepal
Gold and Silver Dealers' Association) and write data/gold-silver.json.

Fails closed, like update_nrb.py: if the page cannot be read or the numbers fail
validation, the existing file is left untouched and the script exits non-zero.

NOTE: the page layout was not checked against the live site when this was written.
If the site changes, this script fails loudly instead of publishing a wrong price.
GOLD_URL / GOLD_OUT can be overridden for testing.
"""
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.request

URL = os.environ.get("GOLD_URL", "https://www.fenegosida.org/")
OUT = os.environ.get("GOLD_OUT", os.path.join(os.path.dirname(__file__), "..", "data", "gold-silver.json"))


def to_text(raw):
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


def find_price(text, label_re):
    """First number of 4+ digits after the label, within 120 characters."""
    m = re.search(label_re + r".{0,120}?(\d{1,3}(?:,\d{2,3})+|\d{4,7})(?:\.\d+)?", text, re.I)
    return int(m.group(1).replace(",", "")) if m else None


def parse(text):
    gold = find_price(text, r"FINE\s+GOLD\s*\(?\s*9999\s*\)?[^0-9]{0,40}?(?:per\s+)?(?:1\s+)?tola")
    silver = find_price(text, r"\bSILVER\b[^0-9]{0,40}?(?:per\s+)?(?:1\s+)?tola")
    return gold, silver


def validate(gold, silver):
    if gold is None or silver is None:
        raise ValueError("price not found on page")
    if not (10_000 <= gold <= 2_000_000):
        raise ValueError("gold price out of plausible range: %s" % gold)
    if not (100 <= silver <= 100_000):
        raise ValueError("silver price out of plausible range: %s" % silver)
    if silver * 20 > gold:
        raise ValueError("silver/gold ratio implausible")
    if os.path.exists(OUT):
        try:
            prev = json.load(open(OUT, encoding="utf-8"))
            pg = prev["gold_per_tola"]
            if abs(gold - pg) / pg > 0.15:
                raise ValueError("gold moved more than 15%% in one update (%s -> %s); refusing to publish" % (pg, gold))
        except (KeyError, ValueError, TypeError) as e:
            if "refusing" in str(e):
                raise


def main():
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "thenepal.io-rates-updater (+https://converter.thenepal.io)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            text = to_text(r.read().decode("utf-8", "replace"))
        gold, silver = parse(text)
        validate(gold, silver)
    except Exception as e:  # noqa: BLE001
        print("Gold/silver update failed, file left unchanged: %s" % e, file=sys.stderr)
        return 1
    now = dt.datetime.now(dt.timezone.utc)
    out = {
        "source": "FENEGOSIDA",
        "source_url": "https://www.fenegosida.org/",
        "gold_per_tola": gold,
        "silver_per_tola": silver,
        "currency": "NPR",
        "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "date": now.astimezone(dt.timezone(dt.timedelta(hours=5, minutes=45))).date().isoformat(),
    }
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    os.replace(tmp, OUT)
    print("wrote gold=%s silver=%s" % (gold, silver))
    return 0


if __name__ == "__main__":
    sys.exit(main())
