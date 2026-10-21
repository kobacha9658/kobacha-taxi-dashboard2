from datetime import datetime
from pathlib import Path
import json
import sys

import requests
from bs4 import BeautifulSoup

URL = "https://transit.yahoo.co.jp/diainfo/area/4"
OUT = Path("data/rail-status.json")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; KobachaTaxiDashboard/1.0; personal status display)"
}


def now_local():
    return datetime.now().astimezone().isoformat(timespec="minutes")


def parse_disruptions(html):
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    if "運行情報" not in page_text and "現在運行情報のある路線" not in page_text:
        raise RuntimeError("運行情報ページを確認できません。ページ構成やアクセス制限が変わった可能性があります")

    found = []
    recognized_rows = 0
    for table in soup.find_all("table"):
        heading = table.find_previous(["h2", "h3"])
        operator = heading.get_text(" ", strip=True) if heading else ""
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) < 2:
                continue
            values = [cell.get_text(" ", strip=True) for cell in cells]
            if values[0] in ("路線", "状況") or values[1] == "状況":
                continue
            line, status = values[0], values[1]
            detail = values[2] if len(values) > 2 else ""
            if not line or not status:
                continue
            # Yahoo's table format has route / status / detail columns.
            if "平常運転" in status or ("事故・遅延情報はありません" in detail and status in ("平常", "平常運転")):
                recognized_rows += 1
                continue
            # Keep only rows that look like route status records, not generic page tables.
            if len(cells) >= 3:
                recognized_rows += 1
                found.append({"operator": operator, "line": line, "status": status, "detail": detail})

    if not found and "事故・遅延情報はありません" not in page_text and recognized_rows == 0:
        raise RuntimeError("運行情報を読み取れませんでした。誤って平常運転と表示しないよう取得を停止しました")
    return found


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ok": False,
        "updated_at": now_local(),
        "source_url": URL,
        "disruptions": [],
    }
    try:
        response = requests.get(URL, headers=HEADERS, timeout=25)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        payload["disruptions"] = parse_disruptions(response.text)
        payload["ok"] = True
        payload["updated_at"] = now_local()
    except Exception as exc:
        payload["message"] = str(exc)[:300]
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Rail status fetch failed: {payload['message']}", file=sys.stderr)
        raise SystemExit(1)

    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated railway status: {len(payload['disruptions'])} disruption(s)")


if __name__ == "__main__":
    main()
