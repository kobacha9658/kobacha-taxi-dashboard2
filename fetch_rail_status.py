#!/usr/bin/env python3
"""Fetch JR East Kanto public service status and publish only disruption entries."""
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
from urllib.request import Request, urlopen
import json, re
from pathlib import Path

URL = "https://traininfo.jreast.co.jp/train_info/kanto.aspx"
OUT = Path("data/rail-status.json")
JST = timezone(timedelta(hours=9))
DISRUPTION = re.compile(r"遅延|運転見合わせ|一部運休|運休|運転中止|運転再開見込|運転再開見込み")
NORMAL = re.compile(r"平常運転")

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"): self.skip += 1
        if tag in ("br", "p", "div", "li", "h1", "h2", "h3", "h4", "section"): self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip: self.skip -= 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "section"): self.parts.append("\n")
    def handle_data(self, data):
        if not self.skip and data.strip(): self.parts.append(data.strip())

def main():
    req = Request(URL, headers={"User-Agent": "KobachaTaxiDashboard/1.0 (public service status link)"})
    with urlopen(req, timeout=25) as r:
        raw = r.read().decode("utf-8", errors="replace")
    parser = TextExtractor(); parser.feed(raw)
    lines = [re.sub(r"\s+", " ", x).strip() for x in "\n".join(parser.parts).splitlines()]
    lines = [x for x in lines if x]
    # Remove duplicate consecutive text fragments and navigation noise.
    unique=[]
    for line in lines:
        if not unique or line != unique[-1]: unique.append(line)
    disruptions=[]
    for i, line in enumerate(unique):
        if not DISRUPTION.search(line):
            continue
        # Status and details are commonly combined in one text node; otherwise use nearby context.
        detail = line
        if len(detail) < 12:
            nearby = " ".join(unique[i+1:i+4])
            if nearby: detail = (detail + " " + nearby).strip()
        # Skip generic explanatory/footer text that is not a current line alert.
        if not re.search(r"線|列車|駅間|方面|区間", detail):
            continue
        if NORMAL.search(detail):
            continue
        if detail not in [x["detail"] for x in disruptions]:
            disruptions.append({"detail": detail[:500], "source": URL})
    # Do not claim normal operation if extraction yielded no alerts: show explicit status.
    payload = {
        "source": URL,
        "source_name": "JR東日本 関東エリア運行情報",
        "checked_at": datetime.now(JST).isoformat(timespec="seconds"),
        "status": "alerts" if disruptions else "no_alerts_found",
        "message": "取得した公開ページから運行異常の記載を抽出しました。公式ページで最新状況をご確認ください。" if disruptions else "公開ページから異常情報を抽出できませんでした。平常運転と断定せず、公式ページで確認してください。",
        "alerts": disruptions,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}: status={payload['status']} alerts={len(disruptions)}")

if __name__ == "__main__": main()
