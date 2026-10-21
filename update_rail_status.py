import json
import re
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

OUT = Path('data/rail-status.json')
URLS = [
    ('関東', 'https://transit.yahoo.co.jp/diainfo/area/4'),
    ('新幹線・特急', 'https://transit.yahoo.co.jp/diainfo/express'),
]

def main():
    items = []
    fetched = []
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; KobachaTaxiDashboard/1.0)'}
    for area, url in URLS:
        r = requests.get(url, headers=headers, timeout=25)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        fetched.append(area)
        # Yahoo's page labels the active-disruption table with this heading.
        heading = soup.find(string=re.compile(r'現在運行情報のある路線'))
        table = heading.find_parent().find_next('table') if heading and heading.find_parent() else None
        if table is None:
            # Fallback: locate a table whose first row looks like route/status/detail.
            for candidate in soup.find_all('table'):
                first = ' '.join(candidate.stripped_strings[:6])
                if '路線' in first and '状況' in first and '詳細' in first:
                    table = candidate
                    break
        if table is None:
            raise RuntimeError(f'{area}: 運行情報テーブルが見つかりません。ページ構造が変更された可能性があります。')
        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all(['th', 'td'])
            if len(cells) < 2:
                continue
            line = ' '.join(cells[0].stripped_strings)
            status = ' '.join(cells[1].stripped_strings)
            detail = ' '.join(cells[2].stripped_strings) if len(cells) > 2 else ''
            if not line or not status or line == '路線':
                continue
            items.append({'operator': area, 'line': line, 'status': status, 'detail': detail})
    result = {
        'ok': True,
        'message': '取得成功',
        'updated_at': datetime.now(timezone.utc).astimezone().isoformat(timespec='minutes'),
        'disruptions': items,
        'sources_checked': fetched,
        'stale': False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {OUT}: {len(items)} rows')

if __name__ == '__main__':
    main()
