"""Fetch the documentary examples used by the static guide.

Run once while building the site; the published pages use only local images.
"""

from __future__ import annotations

import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "GuiaPASE/1.0 (educational static guide; local asset attribution)"}

COMMONS = {
    "harley": "File:Harley-Davidson Advertisement Hot Rod October 1970.jpg",
    "gatorade": "File:Gatorade (14293776364) (Fuel Their Game Win From Within).jpg",
    "cocacola": "File:Coca-Cola 1915 Contour bottle.jpg",
    "hathaway": "File:1951BillBinzenHathawayCampaignAd.jpg",
    "mcdonalds": "File:Mc Donalds sign.jpg",
    "nike": "File:HK Hung Hom 紅磡站 Train Station facade outdoor Ads 曹星如 Rex Tso Sing-Yu October 2017 IX1 Just Do It 01.jpg",
    "amazon": "File:Amazon 1-Click option.png",
    "gmail": "File:Gmail icon (2020).svg",
    "drive": "File:Google Drive icon (2020).svg",
    "maps": "File:Google Maps icon (2020).svg",
    "calendar": "File:Google Calendar icon (2020).svg",
}

OTHER = {
    "volkswagen": {
        "url": "https://thedrum-media.imgix.net/thedrum-user-assets-prod/s3/images/original/16d521e8-2d84-4aa4-8ec6-61bf8f75ceb6-volkswagen-1959-michael-flickr-cc-by-nc-sa-2-0-1764257965.jpg?ar=default&auto=format&dpr=1&fit=max&w=1400",
        "description": "Volkswagen, anuncio Think Small (1959)",
        "credit": "Fotografía del anuncio: Michael / Flickr, CC BY-NC-SA 2.0 (según crédito de The Drum).",
        "source": "https://www.thedrum.com/news/iconic-ads-from-8-decades-of-ddb",
    }
}


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 4:
                raise
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("Download failed")


def plain(value: str) -> str:
    return re.sub(r"<[^>]*>", "", html.unescape(value)).strip()


def save_raster(key: str, data: bytes) -> str:
    image = ImageOps.exif_transpose(Image.open(BytesIO(data))).convert("RGB")
    if image.width > 1900:
        height = round(image.height * 1900 / image.width)
        image = image.resize((1900, height), Image.Resampling.LANCZOS)
    path = OUT / f"{key}.webp"
    image.save(path, "WEBP", quality=84, method=6)
    print(f"{key}: {image.width}×{image.height}, {path.stat().st_size // 1024} KB")
    return f"assets/img/{key}.webp"


def main() -> None:
    credits = []
    for key, title in COMMONS.items():
        params = {
            "action": "query", "format": "json", "titles": title,
            "prop": "imageinfo", "iiprop": "url|extmetadata",
        }
        api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
        result = json.loads(get(api))
        page = next(iter(result["query"]["pages"].values()))
        if "missing" in page:
            print(f"MISSING {title}")
            continue
        info = page["imageinfo"][0]
        existing = OUT / f"{key}.{'svg' if title.lower().endswith('.svg') else 'webp'}"
        data = None if existing.exists() else get(info["url"])
        if title.lower().endswith(".svg"):
            path = OUT / f"{key}.svg"
            if data is not None:
                path.write_bytes(data)
            output = f"assets/img/{key}.svg"
            print(f"{key}: SVG, {path.stat().st_size // 1024} KB")
        else:
            output = save_raster(key, data) if data is not None else f"assets/img/{key}.webp"
        meta = info.get("extmetadata", {})
        credits.append({
            "key": key,
            "file": output,
            "title": title.removeprefix("File:"),
            "source": info["descriptionurl"],
            "author": plain(meta.get("Artist", {}).get("value", "")),
            "license": plain(meta.get("LicenseShortName", {}).get("value", "")),
            "license_url": plain(meta.get("LicenseUrl", {}).get("value", "")),
        })

    for key, item in OTHER.items():
        try:
            data = get(item["url"])
            output = save_raster(key, data)
            credits.append({"key": key, "file": output, **item})
        except Exception as exc:
            print(f"FAILED {key}: {exc}")

    (ROOT / "content" / "creditos-imagenes.json").write_text(
        json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
